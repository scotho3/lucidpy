from pydantic import ValidationError
import pytest
import json
from lucidpy.models import (
    Document,
    Page,
    Rectangle,
    Shape,
    Line,
    LineEndpoint,
    ShapeEndpoint,
    ID,
    Style,
    Stroke,
    Text,
)


def test_shape_model():
    shape = Shape(type="rectangle", id="shape1")
    assert shape.id == "shape1"
    assert shape.type == "rectangle"


def test_rectangle_model():
    rectangle = Rectangle(id="rectangle1")
    assert rectangle.id == "rectangle1"
    assert rectangle.type == "rectangle"


def test_invalid_line_endpoint_position():
    data = {
        "id": "endpoint1",
        "endpointType": "arrow",
        "endpointStyle": "arrow",
        "line_id": "line1",
        "position": 1.5,  # Invalid position
    }

    with pytest.raises(ValidationError):
        LineEndpoint(**data)


def test_valid_id():
    """Test the `validate` method of the `ID` class with a valid ID.

    This test checks if the `validate` method correctly returns the valid ID
    when provided with a valid ID string.

    Assertions:
        - The `validate` method should return the same valid ID string.
    """
    valid_id = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8"
    assert ID.validate(valid_id) == valid_id


def test_invalid_id_length():
    """Test the ID validation for an invalid ID length.

    This test checks that the `ID.validate` method raises a `ValueError`
    when provided with an ID that exceeds the valid length. The invalid
    ID used in this test is 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8x9y0z',
    which is longer than the allowed length. The test expects the error
    message to match 'Invalid ID format'.
    """
    invalid_id = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8x9y0z"
    with pytest.raises(ValueError, match="Invalid ID format"):
        ID.validate(invalid_id)


def test_invalid_id_characters():
    """Test case for validating IDs with invalid characters.

    This test checks that the `ID.validate` method raises a `ValueError`
    when provided with an ID that contains invalid characters. The invalid
    character used in this test is '!', which is not allowed in Lucidchart

    Raises:
        ValueError: If the ID contains invalid characters.
    """
    invalid_id = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8!"
    with pytest.raises(ValueError, match="Invalid ID format"):
        ID.validate(invalid_id)


def test_non_string_id():
    """Test the ID validation for a non-string ID.

    This test checks that the `ID.validate` method raises a `TypeError`
    when provided with a non-string ID. The invalid ID used in this test
    is an integer, which is not allowed. The test expects the error
    message to match 'string required'.
    """
    invalid_id = 1234567890
    with pytest.raises(TypeError, match="string required"):
        ID.validate(invalid_id)


def test_style_fill():
    """Test the fill property of the Style model.

    This test checks if the fill property correctly sets and retrieves the fill color.

    Assertions:
        - The fill color should be set to '#FF0000'.
        - The fill color should be retrieved as '#FF0000'.
    """
    style = Style(fill="#FF0000")

    # style.fill = '#FF0000'
    assert style.fill == {"type": "color", "color": "#FF0000"}


def test_style_stroke():
    """Test the stroke property of the Style model.

    This test checks if the stroke property correctly sets and retrieves the stroke attributes.

    Assertions:
        - The stroke color should be '#000000'.
        - The stroke width should be 1.
        - The stroke style should be 'solid'.
    """
    stroke = Stroke(color="#000000", width=1, style="solid")
    style = Style(stroke=stroke)
    assert style.stroke.color == "#000000"
    assert style.stroke.width == 1
    assert style.stroke.style == "solid"


def test_style_rounding():
    """Test the rounding property of the Style model.

    This test checks if the rounding property correctly sets and retrieves the rounding value.

    Assertions:
        - The rounding value should be 5.
    """
    stroke = Stroke(color="#000000", width=1, style="solid")
    style = Style(stroke=stroke, rounding=5)
    assert style.rounding == 5


def test_stroke_valid_color():
    """Test the Stroke model with a valid color.

    This test checks if the Stroke model correctly parses and stores
    the provided color.

    Assertions:
        - The stroke color should be '#FF0000'.
    """
    stroke = Stroke(color="#FF0000", width=1, style="solid")
    assert stroke.color == "#FF0000"


def test_stroke_invalid_color():
    """Test the Stroke model with an invalid color.

    This test checks that the Stroke model raises a ValidationError
    when an invalid color is provided.

    Assertions:
        - A ValidationError should be raised.
    """
    with pytest.raises(ValidationError):
        Stroke(color="invalid_color", width=1, style="solid")


def test_stroke_valid_width():
    """Test the Stroke model with a valid width.

    This test checks if the Stroke model correctly parses and stores
    the provided width.

    Assertions:
        - The stroke width should be 5.
    """
    stroke = Stroke(color="#000000", width=5, style="solid")
    assert stroke.width == 5


def test_stroke_invalid_width():
    """Test the Stroke model with an invalid width.

    This test checks that the Stroke model raises a ValidationError
    when an invalid width is provided.

    Assertions:
        - A ValidationError should be raised.
    """
    with pytest.raises(ValidationError):
        Stroke(color="#000000", width="invalid_width", style="solid")


def test_stroke_valid_style():
    """Test the Stroke model with a valid style.

    This test checks if the Stroke model correctly parses and stores
    the provided style.

    Assertions:
        - The stroke style should be 'dashed'.
    """
    stroke = Stroke(color="#000000", width=1, style="dashed")
    assert stroke.style == "dashed"


def test_stroke_invalid_style():
    """Test the Stroke model with an invalid style.

    This test checks that the Stroke model raises a ValidationError
    when an invalid style is provided.

    Assertions:
        - A ValidationError should be raised.
    """
    with pytest.raises(ValidationError):
        Stroke(color="#000000", width=1, style="invalid_style")


def test_document_model():
    """Test the Document model with valid data.

    This test checks if the Document model correctly parses and stores
    the provided data. It verifies the version, the number of pages, and
    the title of the first page.

    Assertions:
        - The document version should be 1.
        - The document should contain one page.
        - The title of the first page should be 'Test Page'.
    """
    data = {
        "id": "document1",
        "version": 1,
        "pages": [
            {
                "id": "page1",
                "title": "Test Page",
                "shapes": [
                    {
                        "id": "shape1",
                        "type": "rectangle",
                        "boundingBox": {"x": 0, "y": 0, "w": 100, "h": 100},
                        "style": {
                            "fill": {"type": "color", "color": "#FFFFFF"},
                            "stroke": {"width": 1},
                        },
                        "text": "Sample Shape",
                    }
                ],
                "lines": [],
            }
        ],
    }
    document = Document(**data)
    assert document.version == 1
    assert len(document.pages) == 1
    assert document.pages[0].title == "Test Page"


def test_invalid_document_model():
    data = {
        "version": "invalid_version",  # Invalid type
        "pages": [],
    }
    with pytest.raises(ValidationError):
        Document(**data)


def test_page_model():
    data = {"id": "page1", "title": "Test Page", "shapes": [], "lines": []}
    page = Page(**data)
    assert page.id == "page1"
    assert page.title == "Test Page"


def test_full_document() -> None:
    # create the full document with two shapes and a line connecting them
    document = Document(version=1, pages=[])
    page = Page(title="test-1", id="page1")

    block0_0 = Rectangle(
        id="block0_0",
        boundingBox=dict(x=0, y=0, w=50, h=50),
        style=Style(
            fill=dict(type="color", color="#446070ff"),
            stroke=Stroke(width=0),
        ),
        text="",
    )
    block0_1 = Rectangle(
        id="block0_1",
        boundingBox=dict(x=0, y=50, w=50, h=50),
        style=Style(
            fill=dict(type="color", color="#325a73ff"),
            stroke=Stroke(width=0),
        ),
        text="",
    )
    endpoint1 = ShapeEndpoint(
        shapeId=block0_0,
        position=dict(x=1, y=1),
        style="none",
    )
    endpoint2 = ShapeEndpoint(
        shapeId=block0_1,
        position=dict(x=1, y=1),
        style="none",
    )
    line = Line(
        id="line1",
        type="straight",
        endpoint1=endpoint1,
        endpoint2=endpoint2,
        stroke=Stroke(
            color="#000000",
            width=1,
            style="solid",
        ),
        text=[
            Text(
                text="test",
                position=0.5,
                side="middle",
            )
        ],
    )

    # add the shapes and line to the page
    page.shapes = [block0_0, block0_1]
    page.lines = [line]
    # add the page to the document
    document.pages = [page]

    # check the document is as expected
    with open("tests/assets/example.json") as f:
        expected_data = json.load(f)

    assert json.loads(document.model_dump_json()) == expected_data
