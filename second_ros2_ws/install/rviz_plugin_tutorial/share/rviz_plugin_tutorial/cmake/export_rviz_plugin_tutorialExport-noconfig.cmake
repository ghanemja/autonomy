#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "rviz_plugin_tutorial::point_display" for configuration ""
set_property(TARGET rviz_plugin_tutorial::point_display APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(rviz_plugin_tutorial::point_display PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libpoint_display.so"
  IMPORTED_SONAME_NOCONFIG "libpoint_display.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS rviz_plugin_tutorial::point_display )
list(APPEND _IMPORT_CHECK_FILES_FOR_rviz_plugin_tutorial::point_display "${_IMPORT_PREFIX}/lib/libpoint_display.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
