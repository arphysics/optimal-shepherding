# C++ compiler
cxx=g++-9 -fopenmp

# Compilation flags
cflags=-Wall -pedantic -O3 -std=c++11

# BLAS/LAPACK flags for linear algebra
lp_lflags=-framework Accelerate

# FFTW flags (installed via Homebrew)
fftw_iflags=
fftw_lflags=-lfftw3

# libpng flags (installed via Homebrew)
png_iflags=
png_lflags=-lpng
