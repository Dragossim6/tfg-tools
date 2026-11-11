spec_app_binaries = {
    500: "perlbench_r_base.x86_gem5", 
    502: "cpugcc_r_base.x86_gem5",
    503: "bwaves_r_base.x86_gem5",    
    505: "mcf_r_base.x86_gem5",
    507: "cactusBSSN_r_base.x86_gem5",
    508: "namd_r_base.x86_gem5",
    510: "parest_r_base.x86_gem5",    
    511: "povray_r_base.x86_gem5",
    519: "lbm_r_base.x86_gem5",       
    520: "omnetpp_r_base.x86_gem5",
    521: "wrf_r_base.x86_gem5",       
    523: "cpuxalan_r_base.x86_gem5",
    525: "x264_r_base.x86_gem5",    
    526: "blender_r_base.x86_gem5",
    527: "cam4_r_base.x86_gem5",      
    531: "deepsjeng_r_base.x86_gem5",
    538: "imagick_r_base.x86_gem5",   
    541: "leela_r_base.x86_gem5",
    544: "nab_r_base.x86_gem5",       
    548: "exchange2_r_base.x86_gem5",
    549: "fotonik3d_r_base.x86_gem5", 
    554: "roms_r_base.x86_gem5",
    557: "xz_r_base.x86_gem5"
}

spec_app_input_files = {
    502: "ref32.c",
    503: "bwaves_1.in",
    554: "ocean_benchmark2.in.x"
}

spec_app_output_files = {
    521: "rsl.out.0000"
}

spec_app_arguments = {
    500: ["-I./lib", "checkspam.pl", "2500", "5", "25", "11", "150", "1", "1", "1", "1"],
    502: ["-O3", "-fselective-scheduling", "-fselective-scheduling2", "-o", "ref32.opts..s"],
    505: ["inp.in"],
    507: ["spec_ref.par"],
    508: ["--input", "apoa1.input", "--output", "apoa1.ref.output", "--iterations", "65"],
    510: ["ref.prm"],
    511: ["SPEC-benchmark-ref.pov", "SPEC-benchmark-ref.ini"],
    519: ["3000", "reference.dat", "0", "0", "100_100_130_ldc.of"],
    520: ["-c", "General", "-r", "0"],
    523: ["-v", "t5.xml", "xalanc.xsl"],
    525: ["--pass", "1", "--stats", "x264_stats.log", "--bitrate", "1000", "--frames", "1000", "-o", "BuckBunny_New.264", "BuckBunny.yuv", "1280x720"],
    526: ["sh3_no_char.blend", "--render-output", "sh3_no_char_", "--threads", "1", "-b", "-F", "RAWTGA", "-s", "849", "-e", "849", "-a"],
    531: ["ref.txt"],
    538: ["-limit", "disk", "0", "refrate_input.tga", "-edge", "41", "-resample", "181%", "-emboss", "31", "-colorspace", "YUV", "-mean-shift", "19x19+15%", "-resize", "30%", "refrate_output.tga"],
    541: ["ref.sgf"],
    544: ["1am0", "1122214447", "122"],
    548: ["6"],
    557: ["input.combined.xz", "250", "a841f68f38572a49d86226b7ff5baeb31bd19dc637a922a972b2e6d1257a890f6a544ecab967c313e370478c74f760eb229d4eef8a8d2836d233d3e9dd1430bf", "40401484", "41217675", "7"]
}





