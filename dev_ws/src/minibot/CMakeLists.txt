cmake_minimum_required(VERSION 3.8)
project(minibot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

# install package directories
install(
  DIRECTORY urdf launch rviz worlds config
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
# no package dependencies and no testing for this right now