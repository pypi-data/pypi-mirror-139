# u-cat: Unit conversion for atmospheric trace gases

This is a small Python package to convert between units for the abundance of 
atmospheric trace gases. It supports conversion of point and column measurements.

## Example
```python
import ucat

# convert 10 µg NO2 / m^3 to ppbv
ucat.convert_points(10.0, 'ug m-3', 'ppbv', molar_mass='NO2')

# convert 100 µmol/m² to molecules cm-2
ucat.convert_columns(100, 'umol m-2', 'cm-2', molar_mass='NO2')
```






