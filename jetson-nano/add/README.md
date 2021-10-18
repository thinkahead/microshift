# Cuda add
## Instructions to compile and run the cpu add
Reference https://developer.nvidia.com/blog/even-easier-introduction-cuda/
#### CPU will perform the add on the whole array in a single thread
```
g++ add.cpp -o add
./add
```

## Instructions to compile and run the cuda gpu add
```
export PATH=/usr/local/cuda-10.2/bin:$PATH
```

#### Single thread will perform the add on the whole array
```
nvcc add1.cu -o add1_cuda
nvprof ./add1_cuda
```
Output
```
```

#### Single block with multiple threads
```
nvcc add2.cu -o add2_cuda
nvprof ./add2_cuda
```
Output
```
 GPU activities:  100.00%  12.951ms         1  12.951ms  12.951ms  12.951ms  add(int, float*, float*)
```

#### Multiple blocks (maximum), each block with multiple threads will perform the add
```
nvcc add3.cu -o add3_cuda
nvprof ./add3_cuda
```
Output
```
 GPU activities:  100.00%  4.4776ms         1  4.4776ms  4.4776ms  4.4776ms  add(int, float*, float*)
```

#### Multiple blocks (less blocks), each block with multiple threads using grid-stride loop
```
nvcc add4.cu -o add4_cuda
nvprof ./add4_cuda
```
Output
```
 GPU activities:  100.00%  3.0574ms         1  3.0574ms  3.0574ms  3.0574ms  add(int, float*, float*)
```
