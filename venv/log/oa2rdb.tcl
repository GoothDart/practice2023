source [pr_env_variable EPHYSRESYNTHESIS_TCL]/ephysresynthesis.tcl
set design ar
set device n3xst150f
set design_oa_lib_path /home/dmitriev/data/diamond1/pseudo-device-routing/star_design_large
set design_oa_lib ar_oa
set sdc_file -
set intrinsic_spef_file -
set load_view_name synthesis
pr_set_thread_number 1
source ../.PM/rdb_read.tcl
pr_load_design $device $design $design_oa_lib_path $design_oa_lib $load_view_name $sdc_file $intrinsic_spef_file
pr_save_snapshot [file join .. snapshots ar synthesis layout.rdb]
exit
