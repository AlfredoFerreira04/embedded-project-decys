cmake_minimum_required(VERSION 3.10)
project(decys_serial LANGUAGES CXX)

add_library(serial STATIC
    serial/src/serial.cc
    serial/src/impl/unix.cc
    serial/src/impl/list_ports/list_ports_linux.cc
)

target_include_directories(serial PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/serial/include
)

target_link_libraries(serial PUBLIC
    rt
    pthread
)

add_executable(serial_test serial_pruning.cpp)
target_link_libraries(serial_test PRIVATE serial)