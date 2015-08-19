/*!
 *  @file   theTest.cpp
 *  @brief  Doing my test
 *
 *  Some more detailed description
 *
 *  @author  Daniel Noland (DN), mehner.fritz@fh-swf.de
 *
 *  @internal
 *       Created:  02/02/2015
 *       Version:  -1
 *      Revision:  none
 *      Compiler:  g++
 *  Organization:  University of Colorado at Boulder
 *     Copyright:  Copyleft (ɔ) 2015, Daniel Noland
 *
 * LICENSE: full text available at http://bit.ly/1kwO2IJ
 *
 * THE WORK IS PROVIDED UNDER THE TERMS OF THIS CREATIVE COMMONS PUBLIC LICENSE
 * ("CCPL" OR "LICENSE"). THE WORK IS PROTECTED BY COPYRIGHT AND/OR OTHER
 * APPLICABLE LAW. ANY USE OF THE WORK OTHER THAN AS AUTHORIZED UNDER THIS
 * LICENSE OR COPYRIGHT LAW IS PROHIBITED.
 *
 * BY EXERCISING ANY RIGHTS TO THE WORK PROVIDED HERE, YOU ACCEPT AND AGREE TO
 * BE BOUND BY THE TERMS OF THIS LICENSE. TO THE EXTENT THIS LICENSE MAY BE
 * CONSIDERED TO BE A CONTRACT, THE LICENSOR GRANTS YOU THE RIGHTS CONTAINED
 * HERE IN CONSIDERATION OF YOUR ACCEPTANCE OF SUCH TERMS AND CONDITIONS.
 *
 */

#include <iostream>
#include <fstream>
#include <map>
#include <vector>
#include <string>

struct SomeStruct {
   int a;
   int b;
   int c;
};

int do_something(int a) {
   int b = 4;
   return a + b;
}

int do_something_else(const int* const ary, const int LEN) {
   int sum = 0;
   for(int i = 0; i < LEN; ++i) {
      sum += ary[i];
   }
   return sum;
}

int* dynamic_copy(const int* const ary, const int LEN) {
   int* cpy = new int[LEN];
   for (int i = 0; i < LEN; ++i) {
      cpy[i] = ary[i];
   }
   return cpy;
}

unsigned long fact(const unsigned long n) {
   return n ? n * fact(n - 1) : 1;
}

unsigned long fib(const unsigned long n) {
   if (n <= 1) {
      return 0;
   }
   if (n == 2) {
      return 1;
   }
   unsigned long x = fib(n - 1) + fib(n - 2);
   return x;
}


int main(int argc, char *argv[]) {
   const int COUNT = 12;
   const int INT_ARRAY = 20;
   SomeStruct* structArray = new SomeStruct[COUNT];
   int* array = new int[INT_ARRAY];
   int* array2 = new int[INT_ARRAY];
   int* array4 = new int;
   std::string catParty = "hello world!";
   std::vector<int> myVector = { 6, 2, 3, 7, 5, 4, 1 };
   int quantity = 32;
   for (int i = 0; i < quantity; ++i) {
      myVector.push_back(i);
   }
   for(int i = 0; i < COUNT; ++i) {
      structArray[i].a = 2;
      structArray[i].b = 4;
      structArray[i].c = 13;
   }
   for(int i = 0; i < INT_ARRAY; ++i) {
      array[i] = 14;
      array2[i] = 14;
   }
   int* array3 = new int[INT_ARRAY];
   int q = do_something(array[0]);
   int total = do_something_else(array, INT_ARRAY);
   delete array4;
   array4 = dynamic_copy(array, INT_ARRAY);
   unsigned long someFact = fact(6);
   unsigned long someFib = fib(8);
   for (auto& i : myVector) {
      std::cout << i << std::endl;
   }
   while( ! myVector.empty() ) {
      myVector.pop_back();
   }
   std::cout << catParty << std::endl;
   return 0;
}

