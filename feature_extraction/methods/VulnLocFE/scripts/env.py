import os
analyzer_root = os.getenv('FE_ROOT')
dynamorio_path = analyzer_root+"/deps/dynamorio/bin64/drrun"
iftracer_path = analyzer_root+"/scripts/iftracer/iftracer/libiftracer.so"
iflinetracer_path = analyzer_root+"/scripts/iftracer/ifLineTracer/libifLineTracer.so"
libcbr_path = analyzer_root+"/deps/dynamorio/samples/bin64/libcbr.so"
