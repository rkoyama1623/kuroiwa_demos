project(vector_tutorial)

cmake_minimum_required(VERSION 2.8)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x -Wall")

add_executable(need-zero-iinput-after-delete need-zero-iinput-after-delete.cpp)
