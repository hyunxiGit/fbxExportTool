# fbxExportTool
1. This tool aim to provide a clean and easy-to-use solution for Maya -> Unity animation dtata export pipeline.  
2. This tool supports exporting two sets of data ( model/skeleton & skeleton/animation ) of one character shareing the same bone structure.
1. This FBX exporter currently works with RapidRig 1.8.2‘s Rig naming convention.

to open the tool:
1. set up the tool as normal multi-module python plugin for maya

2. in maya python script tab type:
	import fbxExporterControler as bfxExporter
   	bfxEporter.main

3. you should be able to see the GUI

to export:
1. open the maya file
2. click on one of the rig controller, the tool should be able to tell if this file contrain animation or not
3. you can change export path by typing in the text area and then click save export path btn
4. click export 
