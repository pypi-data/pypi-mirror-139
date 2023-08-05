def page_to_offset(page: int, limit: int) -> int:
    """
    calculate limit for mysql by page and limit
    :param page: page number, 1-based
    :param limit: page size
    :return: sql limit param
    """
    return max([0, page - 1]) * limit


def total_pages(limit: int, total_count: int) -> int:
    """
    calculate total pages by limit and total count
    :param limit: page size
    :param total_count: total record count
    :return: total page count
    """
    return int((total_count - 1) / limit) + 1
