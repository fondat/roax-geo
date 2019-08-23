import pytest
import roax.geo as geo
import roax.schema as s


def test_Point_valid():
    geo.Point().validate({"type": "Point", "coordinates": [100.0, 0.0]})


def test_Point_invalid_type():
    with pytest.raises(s.SchemaError):
        geo.Point().validate({"type": "Zoink", "coordinates": [100.0, 0.0]})


def test_Point_invalid_longitude():
    with pytest.raises(s.SchemaError):
        geo.Point().validate({"type": "Point", "coordinates": [-190.0, 0.0]})


def test_Point_invalid_latitude():
    with pytest.raises(s.SchemaError):
        geo.Point().validate({"type": "Point", "coordinates": [100.0, 91.0]})


def test_LineString_valid():
    geo.LineString().validate(
        {"type": "LineString", "coordinates": [[100.0, 0.0], [101.0, 1.0]]}
    )


def test_Polygon_valid_noholes():
    geo.Polygon().validate(
        {
            "type": "Polygon",
            "coordinates": [
                [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]
            ],
        }
    )


def test_Polygon_valid_withholes():
    geo.Polygon().validate(
        {
            "type": "Polygon",
            "coordinates": [
                [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
                [[100.8, 0.8], [100.8, 0.2], [100.2, 0.2], [100.2, 0.8], [100.8, 0.8]],
            ],
        }
    )


def test_Polygon_invalid_ring():
    with pytest.raises(s.SchemaError):
        geo.Polygon().validate(
            {
                "type": "Polygon",
                "coordinates": [
                    [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0]]
                ],
            }
        )


def test_Polygon_invalid_min_rings_param():
    with pytest.raises(ValueError):
        geo.Polygon(min_rings=0).validate(
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [100.0, 0.0],
                        [101.0, 0.0],
                        [101.0, 1.0],
                        [100.0, 1.0],
                        [100.0, 0.0],
                    ]
                ],
            }
        )


def test_Polygon_invalid_max_rings_param():
    with pytest.raises(ValueError):
        geo.Polygon(min_rings=2, max_rings=1).validate(
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [100.0, 0.0],
                        [101.0, 0.0],
                        [101.0, 1.0],
                        [100.0, 1.0],
                        [100.0, 0.0],
                    ]
                ],
            }
        )


def test_Polygon_invalid_min_rings_value():
    with pytest.raises(s.SchemaError):
        geo.Polygon(min_rings=2).validate(
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [100.0, 0.0],
                        [101.0, 0.0],
                        [101.0, 1.0],
                        [100.0, 1.0],
                        [100.0, 0.0],
                    ]
                ],
            }
        )


def test_Polygon_invalid_max_rings_value():
    with pytest.raises(s.SchemaError):
        geo.Polygon(max_rings=1).validate(
            {
                "type": "Polygon",
                "coordinates": [
                    [
                        [100.0, 0.0],
                        [101.0, 0.0],
                        [101.0, 1.0],
                        [100.0, 1.0],
                        [100.0, 0.0],
                    ],
                    [
                        [100.8, 0.8],
                        [100.8, 0.2],
                        [100.2, 0.2],
                        [100.2, 0.8],
                        [100.8, 0.8],
                    ],
                ],
            }
        )


def test_MultiPoint_valid():
    geo.MultiPoint().validate(
        {"type": "MultiPoint", "coordinates": [[100.0, 0.0], [101.0, 1.0]]}
    )


def test_MultiLineString_valid():
    geo.MultiLineString().validate(
        {
            "type": "MultiLineString",
            "coordinates": [[[100.0, 0.0], [101.0, 1.0]], [[102.0, 2.0], [103.0, 3.0]]],
        }
    )


def test_MultiPolygon_valid():
    geo.MultiPolygon().validate(
        {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [
                        [102.0, 2.0],
                        [103.0, 2.0],
                        [103.0, 3.0],
                        [102.0, 3.0],
                        [102.0, 2.0],
                    ]
                ],
                [
                    [
                        [100.0, 0.0],
                        [101.0, 0.0],
                        [101.0, 1.0],
                        [100.0, 1.0],
                        [100.0, 0.0],
                    ],
                    [
                        [100.2, 0.2],
                        [100.2, 0.8],
                        [100.8, 0.8],
                        [100.8, 0.2],
                        [100.2, 0.2],
                    ],
                ],
            ],
        }
    )


def test_GeometryCollection_valid():
    geo.GeometryCollection().validate(
        {
            "type": "GeometryCollection",
            "geometries": [
                {"type": "Point", "coordinates": [100.0, 0.0]},
                {"type": "LineString", "coordinates": [[101.0, 0.0], [102.0, 1.0]]},
            ],
        }
    )


def test_Feature_valid():
    geo.Feature().validate(
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
            "properties": {"prop0": "value0"},
        }
    )


def test_FeatureCollection_valid():
    geo.FeatureCollection().validate(
        {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
                    "properties": {"prop0": "value0"},
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [102.0, 0.0],
                            [103.0, 1.0],
                            [104.0, 0.0],
                            [105.0, 1.0],
                        ],
                    },
                    "properties": {"prop0": "value0", "prop1": 0.0},
                },
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [100.0, 0.0],
                                [101.0, 0.0],
                                [101.0, 1.0],
                                [100.0, 1.0],
                                [100.0, 0.0],
                            ]
                        ],
                    },
                    "properties": {"prop0": "value0", "prop1": {"this": "that"}},
                },
            ],
        }
    )