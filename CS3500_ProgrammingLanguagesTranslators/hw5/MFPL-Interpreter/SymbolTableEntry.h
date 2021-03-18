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
#define LT '<'
#define GT '>'
#define LE 'L'
#define GE 'G'
#define EQ '='
#define NE '!'
#define AND '&'
#define OR '|'
#define NOT '!'
struct TYPE_INFO {
  int m_intVal;
  char m_strVal[100];
  bool m_boolVal;
  int m_type;
  int m_params;
  int m_returnType;
};

class SYMBOL_TABLE_ENTRY 
{
private:
  // Member variables
  string name;
  TYPE_INFO typeInfo;

public:
  // Constructors
  SYMBOL_TABLE_ENTRY( ) { name = ""; typeInfo.m_type = UNDEFINED; typeInfo.m_params = UNDEFINED; typeInfo.m_returnType = UNDEFINED; strcpy(typeInfo.m_strVal,""); typeInfo.m_boolVal = true; typeInfo.m_intVal = 0;}

  SYMBOL_TABLE_ENTRY(const SYMBOL_TABLE_ENTRY& source) {
    typeInfo.m_type = source.typeInfo.m_type;
    typeInfo.m_params = source.typeInfo.m_params;
    typeInfo.m_returnType = source.typeInfo.m_returnType;
    typeInfo.m_intVal = source.typeInfo.m_intVal;
    typeInfo.m_boolVal = source.typeInfo.m_boolVal;
    //typeInfo.m_strVal = static_cast<char*>(malloc((strlen(source.typeInfo.m_strVal) + 1) * sizeof(char)));
    strcpy(typeInfo.m_strVal, source.typeInfo.m_strVal);
    name = source.name;
  }
  SYMBOL_TABLE_ENTRY(const string theName, const int theType, const int params, const int retType, const int val) 
  {
    name = theName;
    typeInfo.m_type = theType;
    typeInfo.m_params = params;
    typeInfo.m_returnType = retType;
    typeInfo.m_intVal = val;
    strcpy(typeInfo.m_strVal, "");  
    typeInfo.m_boolVal = true;
  }
  SYMBOL_TABLE_ENTRY(const string theName, const int theType, const int params, const int retType, const char val[]) 
  {
    name = theName;
    typeInfo.m_type = theType;
    typeInfo.m_params = params;
    typeInfo.m_returnType = retType;
    typeInfo.m_intVal = UNDEFINED;
    typeInfo.m_boolVal = true;
    strcpy(typeInfo.m_strVal, val);
  }

  SYMBOL_TABLE_ENTRY(const string theName, const int theType, const int params, const int retType, const bool val) 
  {
    name = theName;
    typeInfo.m_type = theType;
    typeInfo.m_params = params;
    typeInfo.m_returnType = retType;
    typeInfo.m_intVal = UNDEFINED;
    strcpy(typeInfo.m_strVal, "");  
    typeInfo.m_boolVal = val;
  }


  SYMBOL_TABLE_ENTRY(const string theName) {
    name = theName;
    typeInfo.m_type = UNDEFINED;
    typeInfo.m_params = UNDEFINED;
    typeInfo.m_returnType = UNDEFINED;
    typeInfo.m_intVal = UNDEFINED;
    typeInfo.m_boolVal = true;
    strcpy(typeInfo.m_strVal, "");
  }
  // Accessors
  string getName() const { return name; }
  TYPE_INFO getTypeInfo() const { return typeInfo; }
};

#endif  // SYMBOL_TABLE_ENTRY_H
