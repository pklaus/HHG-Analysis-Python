#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <cv.h>
#include <highgui.h>

using namespace cv;
using namespace std;

typedef unsigned short int uint16;

int main(int argc, char *argv[])
{
  Mat origImg;

  if(argc<2)
    { printf("Usage: main <image-file-name>\n\7"); exit(0); }

  origImg = imread(argv[1], -1);
  /* cout << "types: " << CV_8UC1 << " " << CV_16UC1 << " " << CV_8UC4 << " " << CV_32SC1 << " " << CV_32FC1 << " " << CV_64FC1 << endl;
  cout << origImg.type() << endl; // 2 = CV_16UC1
  cout << dblImg.type() << endl; // 6 = CV_64FC1 */
  cout << origImg.at<uint16>(100,100) << endl;

  // compute min and max
  uint16 max = 0. , min = 65535;
  MatConstIterator_<uint16> it = origImg.begin<uint16>(), it_end = origImg.end<uint16>();
  for(; it != it_end; ++it) {
    max = std::max(*it, max);
    min = std::min(*it, min);
  }
  cout << "min: " << min << " max: " << max << endl;

  Mat scaledImg = (origImg - min)*static_cast<uint16>(max-min);
  //newImg += 256;

  /*
  // compute min and max
  Mat_<double> dblImg;
  dblImg = origImg;
  cout << dblImg.at<double>(100,100) << endl;
  double max = 0. , min = 65535;
  MatConstIterator_<double> it = dblImg.begin(), it_end = dblImg.end();
  for(; it != it_end; ++it) {
    max = std::max(*it, max);
    min = std::min(*it, min);
  }
  cout << "min: " << min << " max: " << max << endl;
  */

  namedWindow("SRC");
  imshow("SRC", origImg);
  namedWindow("scaled");
  imshow("scaled", scaledImg);

  // wait for a key
  waitKey(0);

  return 0;
}
