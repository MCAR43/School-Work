#ifndef SYMBOL_TABLE_ENTRY_H
#define SYMBOL_TABLE_ENTRY_H

#include <string>
using namespace std;

#define UNDEFINED  -1
#define FUNCTION 0
#define _INT 1                //0001
#define _STR 2                //0010
#define _INT_OR_STR 3         //0011
#define _BOOL 4               //0100
#define _INT_OR_BOOL 5        //0101
#define _STR_OR_BOOL 6        //0110
#define _INT_OR_STR_OR_BOOL 7 //0111
#define NOT_APPLICABLE -1 

#define REL_OP 9
#define LOG_OP 10


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
  TYPE_INFO typeInfo;

public:
  // Constructors
  SYMBOL_TABLE_ENTRY( ) { name = ""; typeInfo.m_type = UNDEFINED; typeInfo.m_params = UNDEFINED; typeInfo.m_returnType = UNDEFINED; }

  SYMBOL_TABLE_ENTRY(const string theName, const int theType, const int params, const int retType) 
  {
    name = theName;
    typeInfo.m_type = theType;
    typeInfo.m_params = params;
    typeInfo.m_returnType = retType;
  }

  SYMBOL_TABLE_ENTRY(const string theName) {
    name = theName;
    typeInfo.m_type = UNDEFINED;
    typeInfo.m_params = UNDEFINED;
    typeInfo.m_returnType = UNDEFINED;
  }

  // Accessors
  string getName() const { return name; }
  TYPE_INFO getTypeInfo() const { return typeInfo; }
};

#endif  // SYMBOL_TABLE_ENTRY_H
