#ifndef SYMBOL_TABLE_ENTRY_H
#define SYMBOL_TABLE_ENTRY_H

#include <string>
using namespace std;

#define UNDEFINED  -1
#define _INT 1
#define _STR 2
#define _INT_OR_STR 3
#define _BOOL 4
#define _INT_OR_BOOL 5
#define _STR_OR_BOOL 6
#define _INT_OR_STR_OR_BOOL 7

typedef struct {
  int m_type;
  int m_params;
  int m_returnType;
} TYPE_INFO;


class SYMBOL_TABLE_ENTRY 
{
private:
  // Member variables
  string name;
  int typeCode;  

public:
  // Constructors
  SYMBOL_TABLE_ENTRY( ) { name = ""; typeCode = UNDEFINED; }

  SYMBOL_TABLE_ENTRY(const string theName, const int theType) 
  {
    name = theName;
    typeCode = theType;
  }

  // Accessors
  string getName() const { return name; }
  int getTypeCode() const { return typeCode; }
};

#endif  // SYMBOL_TABLE_ENTRY_H
