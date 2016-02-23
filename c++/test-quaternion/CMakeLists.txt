project(accumelate_tutorial)

cmake_minimum_required(VERSION 2.8)
set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x -W -Wall")
find_package(cmake_modules REQUIRED)
find_package(Eigen REQUIRED)

include_directories(${EIGEN_INCLUDE_DIRS})

add_executable(test test-quaternion.cpp)
