

ROW_TOLERANCE = 0.01
COLUMN_TOLERANCE = 0.03  # TODO columns do not really work


def get_dimensions(data):
    if len(data["conf"]) < 1:
        return 0, 0

    min_w, min_h, max_w, max_h = \
        data["left"][0], data["top"][0], data["left"][0], data["top"][0]
    for i in range(len(data["conf"])):
        if data["conf"][i] < 0:
            continue

        min_w = min(min_w, data["left"][i])
        min_h = min(min_h, data["top"][i])
        max_w = max(max_w, data["left"][i] + data["width"][i])
        max_h = max(max_h, data["top"][i] + data["height"][i])

    return max_w - min_w, max_h - min_h


def get_document_text(data):
    width, height = get_dimensions(data)
    last_top = 0.0
    current_line = ""
    result = ""

    for i in range(len(data["conf"])):
        if data["conf"][i] < 0:
            continue

        relative_top = data["top"][i] / height
        if abs(relative_top - last_top) > ROW_TOLERANCE:
            if result:
                result += "\n"

            result += current_line
            current_line = f"{data["text"][i]}\t"
            last_top = relative_top
            continue

        current_line += f"{data["text"][i]}\t"

    return result


def get_structured_data(data, page_num):
    width, height = get_dimensions(data)
    last_top = 0.0
    last_left = 0.0
    row_num = 1
    column_num = 1
    current_row = []
    rows = []

    for i in range(len(data["conf"])):
        if data["conf"][i] < 0:
            continue

        relative_top = data["top"][i] / height
        if abs(relative_top - last_top) > ROW_TOLERANCE:
            if current_row:
                rows.extend(current_row)
                row_num += 1
                column_num = 1

            current_row = [
                {
                    "value": data["text"][i],
                    "row": row_num,
                    "column": column_num,
                    "left": data["left"][i],
                    "top": data["top"][i],
                    "width": data["width"][i],
                    "height": data["height"][i]
                }
            ]
            last_top = relative_top
            last_left = (data["left"][i] + data["width"][i]) / width
            continue

        relative_left = data["left"][i] / width
        if abs(relative_left - last_left) > COLUMN_TOLERANCE:
            column_num += 1
            last_left = (data["left"][i] + data["width"][i]) / width

        current_row.append({
            "value": data["text"][i],
            "page": page_num,
            "row": row_num,
            "column": column_num,
            "left": data["left"][i],
            "top": data["top"][i],
            "width": data["width"][i],
            "height": data["height"][i]
        })

    return rows


def process_ocr_data(ocr_data):
    page_num = 1
    result_text = ""
    result_structured_data = []
    for data in ocr_data:
        text = get_document_text(data)
        if result_text:
            result_text += "\n"
        result_text += text
        result_structured_data.extend(get_structured_data(data, page_num))
        page_num += 1
    return result_text, result_structured_data
