from __future__ import annotations

import dataclasses
import datetime
import enum
import logging
import typing

import aiohttp
import bs4
import optext.option
import pandas as pd
import requests

import atcoder.auth
import atcoder.contest
import atcoder.language
import atcoder.scrape

_LOGGER = logging.getLogger(__name__)
REQUEST_CHUNK_SIZE = 10
REQUEST_INTERVAL_SEC = 0


class SubmissionStatus(enum.Enum):
    AC = enum.auto()
    WA = enum.auto()
    RE = enum.auto()
    TLE = enum.auto()
    MLE = enum.auto()
    QLE = enum.auto()
    CE = enum.auto()
    OLE = enum.auto()
    IE = enum.auto()
    WJ = enum.auto()
    WR = enum.auto()
    JUDGING = enum.auto()


def _status_from_str(status: str) -> SubmissionStatus | None:
    return SubmissionStatus.__members__.get(status.upper())


def _status_to_string(status: SubmissionStatus) -> str:
    if status == SubmissionStatus.JUDGING:
        return "Judging"
    else:
        return status.name


class LanguageParseError(Exception):
    pass


def _parse_language(language_text: str) -> atcoder.language.Language:
    language = atcoder.language._language_from_text(language_text)
    if language is not None:
        return language
    (
        language_name,
        compiler_or_runtime,
        *_,
    ) = atcoder.language._parse_language_text(language_text)
    language = atcoder.language._language_from_name(language_name)
    if language is not None:
        return language
    if compiler_or_runtime is None:
        raise LanguageParseError
    return optext.option.unwrap(
        atcoder.language._language_from_compiler(compiler_or_runtime),
    )


@dataclasses.dataclass(frozen=True)
class JudgeResult:
    case_name: str
    status: SubmissionStatus
    exec_time_ms: int
    memory_usage_kb: int


@dataclasses.dataclass(frozen=True)
class Summary:
    datetime: datetime.datetime
    task_id: str
    username: str
    language: atcoder.language.Language
    score: int
    code_size_kb: int
    status: SubmissionStatus
    exec_time_ms: int | None = None
    memory_usage_kb: int | None = None


@dataclasses.dataclass(frozen=True)
class Details:
    code: str
    judge_results: list[JudgeResult] | None = None


@dataclasses.dataclass
class SubmissionResult:
    id: int
    summary: Summary
    details: Details | None = None


async def _get_submission_page(
    session: aiohttp.ClientSession,
    contest_id: str,
    submission_id: int,
) -> aiohttp.ClientResponse:
    url = (
        f"{atcoder.contest._CONTESTS_URL}/{contest_id}"
        f"/submissions/{submission_id}"
    )
    _LOGGER.info(f"get {url}")
    return await session.get(url)


def _scrape_id(html: str) -> int:
    import re

    soup = atcoder.scrape._parse_html(html)
    match = re.match(r"^.*\#(\d+).*$", soup.find(class_="h2").text)
    return int(optext.option.unwrap(match).group(1))


def _scrape_summary(html: str) -> Summary:
    import datetime

    soup = atcoder.scrape._parse_html(html)
    infos = soup.table.find_all("tr")
    assert len(infos) >= 7
    if soup.table.find(class_="waiting-judge") is not None:
        status = SubmissionStatus.WJ
    else:
        status = optext.option.unwrap(
            _status_from_str(infos[6].td.text.split()[-1]),
        )
    if len(infos) == 9:
        exec_time_ms = atcoder.scrape._strip_unit(infos[7].td.text)
        memory_usage_kb = atcoder.scrape._strip_unit(infos[8].td.text)
    else:
        exec_time_ms = None
        memory_usage_kb = None
    return Summary(
        datetime=datetime.datetime.strptime(
            infos[0].time.text,
            "%Y-%m-%d %H:%M:%S%z",
        ),
        task_id=infos[1].a.get("href").split("/")[-1],
        username=infos[2].a.get("href").split("/")[-1],
        language=_parse_language(infos[3].td.text.strip()),
        score=int(infos[4].td.text),
        code_size_kb=atcoder.scrape._strip_unit(infos[5].td.text),
        status=status,
        exec_time_ms=exec_time_ms,
        memory_usage_kb=memory_usage_kb,
    )


def _scrape_code(html: str) -> str:
    soup = atcoder.scrape._parse_html(html)
    return typing.cast(str, soup.find(id="submission-code").text)


def _scrape_judge_results(
    html: str,
) -> list[JudgeResult] | None:
    tables = pd.read_html(html)
    if len(tables) <= 3:  # no judge results.
        return None
    table = tables[-1]
    table.rename(
        columns={
            "Case Name": "case_name",
            "Status": "status",
            "Exec Time": "exec_time_ms",
            "Memory": "memory_usage_kb",
        },
        inplace=True,
    )
    table["exec_time_ms"] = table["exec_time_ms"].map(
        atcoder.scrape._strip_unit
    )
    table["memory_usage_kb"] = table["memory_usage_kb"].map(
        atcoder.scrape._strip_unit
    )
    table["status"] = table["status"].map(_status_from_str)
    records = table.to_dict(orient="records")
    return [JudgeResult(**record) for record in records]


def _scrape_details(html: str) -> Details:
    return Details(
        code=_scrape_code(html),
        judge_results=_scrape_judge_results(html),
    )


def _scrape_submission_result(html: str) -> SubmissionResult:
    return SubmissionResult(
        id=_scrape_id(html),
        summary=_scrape_summary(html),
        details=_scrape_details(html),
    )


@dataclasses.dataclass
class SubmissionsSearchParams:
    task_id: str | None = None
    language_category: str | None = None
    language_id: int | None = None
    status: str | None = None
    username: str | None = None


_TO_URL_PARAMS: typing.Final[dict[str, str]] = {
    "task_id": "f.Task",
    "language_category": "f.LanguageName",
    "language_id": "f.Language",
    "status": "f.Status",
    "username": "f.User",
}


def _to_url_param(param: str) -> str | None:
    return _TO_URL_PARAMS.get(param)


def _make_url_params(
    search_params: SubmissionsSearchParams | None = None,
    page: int | None = None,
) -> dict[str, str | int]:
    url_params: dict[str, str | int] = dict()
    if search_params is not None:
        for param, value in dataclasses.asdict(search_params).items():
            if value is None:
                continue
            url_params[optext.option.unwrap(_to_url_param(param))] = value
    if page is not None:
        url_params["page"] = page
    return url_params


async def _get_submissions_page(
    session: aiohttp.ClientSession,
    contest_id: str,
    search_params: SubmissionsSearchParams | None = None,
    page: int | None = None,
) -> aiohttp.ClientResponse:
    url = f"{atcoder.contest._CONTESTS_URL}/{contest_id}/submissions"
    _LOGGER.info(f"get {url}, page: {page}")
    return await session.get(
        url,
        params=_make_url_params(search_params, page),
    )


def _get_my_submissions_page(
    session: requests.Session,
    contest_id: str,
    search_params: SubmissionsSearchParams | None = None,
    page_id: int | None = None,
) -> requests.Response:
    url = f"{atcoder.contest._CONTESTS_URL}/{contest_id}/submissions/me"
    _LOGGER.info(f"get {url}")
    return session.get(
        url=url,
        params=_make_url_params(search_params, page_id),
    )


def _scrape_task_ids(html: str) -> list[str]:
    return optext.option.unwrap(
        atcoder.scrape._scrape_html_options(html, "select-task")
    )


def _scrape_language_categories(html: str) -> list[str]:
    return optext.option.unwrap(
        atcoder.scrape._scrape_html_options(html, "select-language")
    )


def _scrape_submission_statuses(html: str) -> list[str]:
    return optext.option.unwrap(
        atcoder.scrape._scrape_html_options(html, "select-status")
    )


def _scrape_pagination(html: str) -> atcoder.scrape.Pagination | None:
    soup = atcoder.scrape._parse_html(html)
    pagination = soup.find(class_="pagination")
    if pagination is None:
        return None
    pages = pagination.find_all("li")
    if not pages:
        _LOGGER.info("no submissions")
        return None
    _LOGGER.info(f"found {len(pages)} pages")
    current_page = int(pagination.find(class_="active").text)
    last_page = int(pages[-1].text)
    return atcoder.scrape.Pagination(current_page, last_page)


def _scrape_submission_row(row: bs4.element.Tag) -> SubmissionResult:
    infos = row.find_all("td")
    assert len(infos) >= 8
    if row.find(class_="waiting-judge") is not None:
        status = SubmissionStatus.WJ
    else:
        status = optext.option.unwrap(
            _status_from_str(infos[6].text.split()[-1])
        )
    if len(infos) == 10:
        exec_time_ms = atcoder.scrape._strip_unit(infos[7].text)
        memory_usage_kb = atcoder.scrape._strip_unit(infos[8].text)
    else:
        exec_time_ms = None
        memory_usage_kb = None
    summary = Summary(
        datetime=datetime.datetime.strptime(
            infos[0].time.text,
            "%Y-%m-%d %H:%M:%S%z",
        ),
        task_id=infos[1].a.get("href").split("/")[-1],
        username=infos[2].a.get("href").split("/")[-1],
        language=_parse_language(infos[3].text.strip()),
        score=int(infos[4].text),
        code_size_kb=atcoder.scrape._strip_unit(infos[5].text),
        status=status,
        exec_time_ms=exec_time_ms,
        memory_usage_kb=memory_usage_kb,
    )
    return SubmissionResult(
        id=infos[-1].a.get("href").split("/")[-1],
        summary=summary,
    )


def _scrape_submissions(html: str) -> list[SubmissionResult] | None:
    soup = atcoder.scrape._parse_html(html)
    if soup.table is None:
        return None
    return [_scrape_submission_row(row) for row in soup.tbody.find_all("tr")]


async def fetch_submission_details(
    session: aiohttp.ClientSession,
    contest_id: str,
    submission_id: int,
) -> SubmissionResult:
    response = await _get_submission_page(session, contest_id, submission_id)
    return _scrape_submission_result(await response.text())


async def _fetch_submissions_page_count(
    session: aiohttp.ClientSession,
    contest_id: str,
    params: SubmissionsSearchParams | None = None,
) -> int:
    response = await _get_submissions_page(session, contest_id, params)
    pagination = _scrape_pagination(await response.text())
    return 0 if pagination is None else pagination.last


async def fetch_submissions(
    session: aiohttp.ClientSession,
    contest_id: str,
    params: SubmissionsSearchParams | None = None,
    page: int | None = None,
) -> list[SubmissionResult] | None:
    response = await _get_submissions_page(session, contest_id, params, page)
    _LOGGER.info(f"fetch: submissions for {contest_id} page: {page}.")
    return _scrape_submissions(await response.text())


async def fetch_all_submissions(
    session: aiohttp.ClientSession,
    contest_id: str,
    params: SubmissionsSearchParams | None = None,
) -> typing.AsyncIterator[SubmissionResult]:
    page = 1
    while True:
        submissions = await fetch_submissions(
            session,
            contest_id,
            params,
            page,
        )
        if submissions is None:
            return
        for submission in submissions:
            yield submission
        page += 1


def fetch_my_submissions(
    session: requests.Session,
    contest_id: str,
    params: SubmissionsSearchParams | None = None,
    page: int | None = None,
) -> list[SubmissionResult] | None:
    if not atcoder.auth._is_logged_in(session):
        raise atcoder.auth.InvalidSessionError
    response = _get_my_submissions_page(session, contest_id, params, page)
    _LOGGER.info(f"fetch: submissions for {contest_id}.")
    return _scrape_submissions(response.text)


def fetch_all_my_submissions(
    session: requests.Session,
    contest_id: str,
    params: SubmissionsSearchParams | None = None,
) -> typing.Iterator[SubmissionResult]:
    page = 1
    while True:
        submissions = fetch_my_submissions(
            session,
            contest_id,
            params,
            page,
        )
        if submissions is None:
            return
        for submission in submissions:
            yield submission
        page += 1


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
