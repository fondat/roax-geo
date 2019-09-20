import geojson
import pytest
import roax.geo
import roax.schema as s


def _test_str_bin(schema, value):
    assert schema.str_decode(schema.str_encode(value)) == value
    assert schema.bin_decode(schema.bin_encode(value)) == value


_point = geojson.Point([100.0, 0.0])


def test_Point_valid():
    roax.geo.Point().validate(_point)


def test_Point_str_bin():
    _test_str_bin(roax.geo.Point(), _point)


def test_Point_str_bin_bbox():
    schema = roax.geo.Point()
    value = schema.json_decode(
        {**_point.__geo_interface__, "bbox": [-101.0, -101.0, 101.0, 101.0]}
    )
    assert schema.str_decode(schema.str_encode(value)) == _point
    assert schema.bin_decode(schema.bin_encode(value)) == _point


def test_Point_bin_meta():
    roax.geo.Point().bin_decode(
        b"\x01\x01\x00\x00 \xe6\x10\x00\x00\x00\x00\x00\x00\x00\x00Y@\x00\x00\x00\x00\x00\x00\x00\x00"
    )


def test_Point_json_decode_invalid():
    with pytest.raises(s.SchemaError):
        roax.geo.Point().json_decode({"type": "Zoink", "coordinates": [100.0, 0.0]})


def test_Point_str_decode_invalid():
    with pytest.raises(s.SchemaError):
        roax.geo.Point().str_decode("POINT(X Y)")


def test_Point_bin_decode_invalid():
    with pytest.raises(s.SchemaError):
        roax.geo.Point().bin_decode(b"1234567890")


def test_Point_invalid_longitude():
    with pytest.raises(s.SchemaError):
        roax.geo.Point().validate(geojson.Point([-190.0, 0.0]))


def test_Point_invalid_latitude():
    with pytest.raises(s.SchemaError):
        roax.geo.Point().validate(geojson.Point([100.0, 91.0]))


_linestring = geojson.LineString([[100.0, 0.0], [101.0, 1.0]])


def test_LineString_valid():
    roax.geo.LineString().validate(_linestring)


def test_LineString_str_bin():
    _test_str_bin(roax.geo.LineString(), _linestring)


def test_Polygon_valid_noholes():
    roax.geo.Polygon().validate(
        geojson.Polygon(
            [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]]
        )
    )


_polygon_holes = geojson.Polygon(
    [
        [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
        [[100.8, 0.8], [100.8, 0.2], [100.2, 0.2], [100.2, 0.8], [100.8, 0.8]],
    ]
)


def test_Polygon_valid_withholes():
    roax.geo.Polygon().validate(_polygon_holes)


def test_Polygon_str_bin():
    _test_str_bin(roax.geo.Polygon(), _polygon_holes)


def test_Polygon_invalid_ring():
    with pytest.raises(s.SchemaError):
        roax.geo.Polygon().validate(
            geojson.Polygon([[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0]]])
        )


def test_Polygon_invalid_min_rings_param():
    with pytest.raises(ValueError):
        roax.geo.Polygon(min_rings=0).validate(
            geojson.Polygon(
                [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]]
            )
        )


def test_Polygon_invalid_max_rings_param():
    with pytest.raises(ValueError):
        roax.geo.Polygon(min_rings=2, max_rings=1).validate(
            geojson.Polygon(
                [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]]
            )
        )


def test_Polygon_invalid_min_rings_value():
    with pytest.raises(s.SchemaError):
        roax.geo.Polygon(min_rings=2).validate(
            geojson.Polygon(
                [[[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]]]
            )
        )


def test_Polygon_invalid_max_rings_value():
    with pytest.raises(s.SchemaError):
        roax.geo.Polygon(max_rings=1).validate(
            geojson.Polygon(
                [
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
                ]
            )
        )


_multipoint = geojson.MultiPoint([[100.0, 0.0], [101.0, 1.0]])


def test_MultiPoint_valid():
    roax.geo.MultiPoint().validate(_multipoint)


def test_MultiPoint_str_bin():
    _test_str_bin(roax.geo.MultiPoint(), _multipoint)


_multilinestring = geojson.MultiLineString(
    [[[100.0, 0.0], [101.0, 1.0]], [[102.0, 2.0], [103.0, 3.0]]]
)


def test_MultiLineString_valid():
    roax.geo.MultiLineString().validate(_multilinestring)


def test_MultiLineString_str_bin():
    _test_str_bin(roax.geo.MultiLineString(), _multilinestring)


_multipolygon = geojson.MultiPolygon(
    [
        [[[102.0, 2.0], [103.0, 2.0], [103.0, 3.0], [102.0, 3.0], [102.0, 2.0]]],
        [
            [[100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0]],
            [[100.2, 0.2], [100.2, 0.8], [100.8, 0.8], [100.8, 0.2], [100.2, 0.2]],
        ],
    ]
)


def test_MultiPolygon_valid():
    roax.geo.MultiPolygon().validate(_multipolygon)


def test_MultiPolygon_str_bin():
    _test_str_bin(roax.geo.MultiPolygon(), _multipolygon)


_geometrycollection = geojson.GeometryCollection(
    [geojson.Point([100.0, 0.0]), geojson.LineString([[101.0, 0.0], [102.0, 1.0]])]
)


def test_GeometryCollection_valid():
    roax.geo.GeometryCollection().validate(_geometrycollection)


def test_GeometryCollection_str_bin():
    _test_str_bin(roax.geo.GeometryCollection(), _geometrycollection)


def test_Feature_valid():
    roax.geo.Feature().validate(
        geojson.Feature(
            geometry=geojson.Point([102.0, 0.5]), properties={"prop0": "value0"}
        )
    )


def test_FeatureCollection_valid():
    roax.geo.FeatureCollection().validate(
        geojson.FeatureCollection(
            [
                geojson.Feature(
                    geometry=geojson.Point([102.0, 0.5]), properties={"prop0": "value0"}
                ),
                geojson.Feature(
                    geometry=geojson.LineString(
                        [[102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]]
                    ),
                    properties={"prop0": "value0", "prop1": 0.0},
                ),
                geojson.Feature(
                    geometry=geojson.Polygon(
                        [
                            [
                                [100.0, 0.0],
                                [101.0, 0.0],
                                [101.0, 1.0],
                                [100.0, 1.0],
                                [100.0, 0.0],
                            ]
                        ]
                    ),
                    properties={"prop0": "value0", "prop1": {"this": "that"}},
                ),
            ]
        )
    )
