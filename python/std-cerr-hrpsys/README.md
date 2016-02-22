```c++
std::ofstream ofs("/tmp/gyro.txt", std::ios::out | std::ios::app);
if (flag) {
  ofs.precision(6);
  ofs.setf(std::ios::fixed);
  ofs << u << ", " << _z << ", ";
 }
 ```
とすると，ファイルに吐ける．
