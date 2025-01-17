import json
import re
from typing import List, Literal, Optional, Any, Union
from pydantic import BaseModel, Field, field_validator, model_validator


class Color(str):
    """A string type that matches the Lucidchart color pattern.

    A hexadecimal color code, e.g., '#RRGGBB' or '#RGB'.
    """

    @classmethod
    def __get_validators__(cls):  # noqa
        yield cls.validate

    @classmethod
    def validate(cls, v, values=None, config=None, field=None):
        """Validate that the color is a valid hexadecimal color code."""
        if not isinstance(v, str):
            raise TypeError("string required")
        if not re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", v):
            raise ValueError("Invalid color format")
        return v


class ID(str):
    """A string type that matches the Lucidchart ID pattern.

    36 characters long, alphanumeric, and containing only -, _, ., and ~.
    """

    @classmethod
    def __get_validators__(cls):  # noqa
        yield cls.validate

    @classmethod
    def validate(cls, v, values=None, config=None, field=None):
        """Validate that the ID is 36 characters long and contains only valid characters."""
        if not isinstance(v, str):
            raise TypeError("string required")
        if not re.match(r"^[a-zA-Z0-9\-\_\.\~]{1,36}$", v):
            raise ValueError("Invalid ID format")
        return v


class _LucidBase(BaseModel):
    def model_dump_json(self, *, indent=True, ignore_null=True) -> str:
        def recursive_model_dump(obj: Any) -> Any:
            if isinstance(obj, BaseModel):
                return {
                    k: recursive_model_dump(v)
                    for k, v in obj.__dict__.items()
                    if v is not None or not ignore_null or v == 0
                }
            elif isinstance(obj, list):
                return [
                    recursive_model_dump(item)
                    for item in obj
                    if item is not None or not ignore_null or item == 0
                ]
            elif isinstance(obj, dict):
                return {
                    key: recursive_model_dump(value)
                    for key, value in obj.items()
                    if value is not None or not ignore_null or value == 0
                }
            else:
                return obj

        data = recursive_model_dump(self)
        return json.dumps(data, indent=indent)


class LucidBase(_LucidBase):
    """Base model for Lucid entities."""

    id: ID


class Stroke(_LucidBase):
    """Stroke model to define the look of a line or border.

    Attributes:
        color (str): The color of the stroke in hexadecimal format (e.g., '#RRGGBB' or '#RGB').
        width (int): The width of the stroke.
        style (Literal['solid', 'dashed', 'dotted']): The style of the stroke, which can be 'solid',
        'dashed', or 'dotted'.
    """

    width: int = None
    color: str = Field(default=None, pattern=r"^#(?:[0-9a-fA-F]{3}){1,2}$")
    style: Literal["solid", "dashed", "dotted"] = None


class Style(_LucidBase):
    """Style model to define the look of a shape or line."""

    fill: Union[str, dict] = Field(
        default_factory=lambda: {"type": "color", "color": "#ffffff"}
    )
    stroke: Optional[Stroke] = Stroke(color="#000000", width=1, style="solid")
    rounding: Optional[int] = None

    @field_validator("fill", mode="before")
    def validate_fill(cls, v):
        if isinstance(v, str):
            return {"type": "color", "color": v}
        return v


class Shape(LucidBase):
    # actions: Optional[List[dict]] = []
    # customData: Optional[List[dict]] = []
    # linkedData: Optional[List[dict]] = []
    type: Literal[
        "rectangle",
        "circle",
        "cloud",
        "diamond",
        "cross",
        "hexagon",
        "octagon",
        "isocolesTriangle",
        "rightTriangle",
    ]
    text: Optional[str] = ""
    style: Style = Style()
    opacity: Optional[int] = None
    note: Optional[str] = None
    boundingBox: dict = {"x": 0, "y": 0, "w": 50, "h": 50}


class Rectangle(Shape):
    type: str = "rectangle"


class Circle(Shape):
    type: str = "circle"


class Cloud(Shape):
    type: str = "cloud"


class Diamond(Shape):
    type: str = "diamond"


class Hexagon(Shape):
    type: str = "hexagon"


class Octagon(Shape):
    type: str = "octagon"


class IsocolesTriangle(Shape):
    type: str = "isocolesTriangle"


class RightTriangle(Shape):
    type: str = "rightTriangle"


class Cross(Shape):
    """Represents a cross shape in Lucidchart.

    Attributes:
        x (float): Horizontal indent, must be between 0.0 and 0.5.
        y (float): Vertical indent, must be between 0.0 and 0.5.
    """

    type: str = "cross"
    x: Optional[float] = 0
    y: Optional[float] = 0

    @field_validator("x", "y")
    def indent_must_be_between_0_and_0_5(cls, v, field):
        """Validate that the indent is between 0.0 and 0.5."""
        if v is not None and not (0.0 <= v <= 0.5):
            raise ValueError(f"{field.name} must be between 0.0 and 0.5")
        return v


class Endpoint(BaseModel):
    """Generic Endpoint model.

    This shouldn't be used directly, but rather as a base class for more specific endpoint types.

    Ref: https://developer.lucid.co/docs/lines-si#endpoint-type

    Args:
        _type_ (str): The type of the endpoint.
        _style_ (str): The style of the endpoint.
    """

    type: str
    style: Literal[
        "none",
        "aggregation",
        "arrow",
        "hollowArrow",
        "openArrow",
        "async1",
        "async2",
        "closedSquare",
        "openSquare",
        "bpmnConditional",
        "bpmnDefault",
        "closedCircle",
        "openCircle",
        "composition",
        "exactlyOne",
        "generalization",
        "many",
        "nesting",
        "one",
        "oneOrMore",
        "zeroOrMore",
        "zeroOrOne",
    ] = "arrow"


class Text(BaseModel):
    """Text used in the Line model.

    Attributes:
        text (str): The text to display.
        position (float): The position of the text on the line (0.0-1.0).
        side (Literal['top', 'middle', 'bottom']): The side of the line where the text should appear.
    """

    text: str
    position: float = Field(0.5, ge=0.0, le=1.0)
    side: Literal["top", "middle", "bottom"] = "middle"


class Line(LucidBase):
    """Represents a Line model in the Lucid system.

    Attributes:
        type (Literal['straight', 'curved', 'elbow']): The type of the line.
        endpoint1 (Endpoint): The first endpoint of the line.
        endpoint2 (Endpoint): The second endpoint of the line.
        stroke (dict): Dictionary containing stroke properties of the line.
        text (List[Text]): List of Text objects associated with the line.
        endpoints (List[Endpoint]): List of Endpoint objects associated with the line.
    """

    lineType: Literal["straight", "curved", "elbow"] = "straight"
    endpoint1: Endpoint
    endpoint2: Endpoint
    stroke: Stroke = Stroke()
    text: List[Text] = [None]

    def connect_shapes(
        self, shape1: Shape, shape2: Shape, stroke: Stroke = Stroke(), text=None
    ):
        """Connect two shapes with the line.

        Args:
            shape1 (Shape): The first shape to connect.
            shape2 (Shape): The second shape to connect.
            stroke (Stroke): The stroke style to use for the line.
            text (Optional[str]): The text to display on the line.
        """
        self.endpoint1 = ShapeEndpoint(shape=shape1)
        self.endpoint2 = ShapeEndpoint(shape=shape2)


class LineEndpoint(Endpoint):
    """Represents an endpoint on a line.

    Attributes:
        line_id (ID): The id for which line to attach the endpoint to.
        position (float): A relative position specifying where on the target line this endpoint
        should attach (must be between 0.0-1.0 inclusive).
    """

    type: str = "lineEndpoint"
    line: Optional[Line]
    line_id: ID = Field(...)
    position: float

    @field_validator("position")
    def position_must_be_between_0_and_1(cls, v):
        """Validate that the position is between 0.0 and 1.0."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("position must be between 0.0 and 1.0")
        return v


class ShapeEndpoint(Endpoint):
    """Represents an endpoint on a shape.

    Attributes:
        shapeId (ID): The ID of the shape to attach the endpoint to. Can also accept a Shape instance.
        position (dict): The position on the shape where the endpoint is attached.
    """

    type: str = "shapeEndpoint"
    shapeId: Optional[Union[ID, Shape]]
    position: dict = Field(default_factory=lambda: {"x": 0.5, "y": 0.5})

    @model_validator(mode="before")
    def check_shape_or_shapeId(cls, values):
        shapeId = values.get("shapeId")
        if isinstance(shapeId, Shape):
            values["shapeId"] = shapeId.id
        elif not isinstance(shapeId, ID):
            raise ValueError("shape_id must be an instance of ID or Shape")
        return values

    @field_validator("position")
    def position_must_be_valid(cls, v):
        """Validate that the position is a dict with x and y between 0.0 and 1.0."""
        if not isinstance(v, dict):
            raise ValueError("position must be a dictionary")
        if "x" not in v or "y" not in v:
            raise ValueError("position must contain x and y coordinates")
        if not (0.0 <= v["x"] <= 1.0 and 0.0 <= v["y"] <= 1.0):
            raise ValueError("x and y must be between 0.0 and 1.0")
        return v


class Page(LucidBase):
    title: str
    # settings: Optional[dict] = {}
    # dataBackedShapes: Optional[List[dict]] = []
    # groups: Optional[List[dict]] = []
    # layers: Optional[List[dict]] = []
    # customData: Optional[List[dict]] = []
    shapes: List[Shape] = []
    lines: List[Line] = []


class Document(_LucidBase):
    version: int = 1
    pages: List[Page]
