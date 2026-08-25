import json
import shutil
import click


def _response_text(result):
    if result.error:
        return f"ERROR\n{result.error}"
    return result.response.text()


def result_lines(result):
    lines = [f"Model: {result.model_id}", "-" * (len(result.model_id) + 7)]
    lines.extend(_response_text(result).splitlines() or [""])
    return lines


def truncate(value, width):
    if len(value) <= width:
        return value
    if width <= 3:
        return value[:width]
    return value[: width - 3] + "..."


def display_side_by_side(results):
    left, right = results
    left_lines, right_lines = result_lines(left), result_lines(right)
    width = shutil.get_terminal_size((120, 20)).columns
    column_width = max(20, (width - 3) // 2)
    click.echo()
    for i in range(max(len(left_lines), len(right_lines))):
        a = left_lines[i] if i < len(left_lines) else ""
        b = right_lines[i] if i < len(right_lines) else ""
        click.echo(
            f"{truncate(a, column_width):<{column_width}} | {truncate(b, column_width):<{column_width}}"
        )
    click.echo()


def display_one_by_one(results):
    for result in results:
        click.echo(f"Model: {result.model_id}")
        click.echo("=" * 60)
        click.echo(_response_text(result))
        click.echo()


def display_json(results):
    payload = []
    for result in results:
        item = {"model": result.model_id}
        if result.error:
            item["error"] = result.error
        else:
            item["response"] = result.response.text()
        payload.append(item)
    click.echo(json.dumps(payload, indent=2))
