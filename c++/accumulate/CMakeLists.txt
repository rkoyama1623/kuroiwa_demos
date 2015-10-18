project(accumelate_tutorial)

cmake_minimum_required(VERSION 2.8)
set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

find_package(Eigen REQUIRED)

include_directories(${EIGEN_INCLUDE_DIRS})
add_library(coordinates coordinates.cpp)

add_executable(accumelate test-accumelate.cpp)
target_link_libraries(accumelate coordinates)
