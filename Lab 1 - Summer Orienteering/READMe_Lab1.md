<h1>CSCI630 - Lab 1</h1>
<h2>Summer Orienteering.</h2>

<br>

<h3> Execution Instructions </h3>
<p> The directory <b>testcases</b> contains various testcases with their README 
files. The final distances are approximately accurate for most cases but can 
vary depending on calculation and methodology.<br><br>
Run the python file lab1.py from the commandline using below template : <br>
>python lab1.py {terrain.png} {mpp.txt} {path.txt} {outImage.png}<br>

where - 
<ol>

1. terrain.png - 395*500 image of the terrain for the test case.
2. mpp.txt - Elevation file, a text representation of the elevations within 
   an area (500 lines of 400 double values, each representing an elevation 
   in meters.
3. path.txt - Waypoints of the orienteering path to be charted.
4. outImage.png - Output image with the path charted.

NOTE : All the paths in the arguments are relative to the source root. Refer to 
CSCI630 - Lab 1 Report for more details.
</ol>