"""
Reusable utilities for the reports app.
"""


def _convert_degrees_to_decimal(degrees_tuple, ref):
    """
    Convert EXIF (degrees, minutes, seconds) tuple to decimal.
    Each component can be (numerator, denominator) or a number.
    ref is 'N'/'S' for latitude or 'E'/'W' for longitude.
    """
    if not degrees_tuple or len(degrees_tuple) != 3:
        return None
    result = 0.0
    for i, component in enumerate(degrees_tuple):
        if hasattr(component, "numerator"):
            val = component.numerator / component.denominator
        elif isinstance(component, (int, float)):
            val = float(component)
        else:
            try:
                num, denom = component
                val = num / denom
            except (TypeError, ValueError, ZeroDivisionError):
                return None
        result += val / (60**i)  # degrees: /1, minutes: /60, seconds: /3600
    if ref in ("S", "W"):
        result = -result
    return result


def extract_gps_from_image(image_path):
    """
    Extract GPS latitude and longitude from an image's EXIF metadata.

    Uses Pillow to read EXIF, parses the GPS IFD, and converts coordinates
    to decimal degrees.

    Args:
        image_path: Path to the image file (str or pathlib.Path).

    Returns:
        Tuple[Optional[float], Optional[float]]: (latitude, longitude) in
        decimal degrees, or (None, None) if GPS data is missing or unreadable.
    """
    try:
        from PIL import Image
    except ImportError:
        return (None, None)

    try:
        with Image.open(image_path) as img:
            exif = img.getexif()
            if exif is None:
                return (None, None)

            # GPS IFD tag
            gps_tag = 34853
            gps_ifd = exif.get_ifd(gps_tag)
            if not gps_ifd:
                return (None, None)

            # 1=GPSLatitudeRef, 2=GPSLatitude, 3=GPSLongitudeRef, 4=GPSLongitude
            lat_ref = gps_ifd.get(1)
            lat_tuple = gps_ifd.get(2)
            lon_ref = gps_ifd.get(3)
            lon_tuple = gps_ifd.get(4)

            if not all([lat_ref, lat_tuple, lon_ref, lon_tuple]):
                return (None, None)

            # Ensure string refs
            lat_ref = lat_ref.decode() if isinstance(lat_ref, bytes) else lat_ref
            lon_ref = lon_ref.decode() if isinstance(lon_ref, bytes) else lon_ref

            latitude = _convert_degrees_to_decimal(lat_tuple, lat_ref)
            longitude = _convert_degrees_to_decimal(lon_tuple, lon_ref)

            if latitude is None or longitude is None:
                return (None, None)
            return (latitude, longitude)

    except (
        OSError,
        IOError,
        KeyError,
        TypeError,
        ValueError,
        ZeroDivisionError,
        AttributeError,
    ):
        return (None, None)
