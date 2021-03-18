#include <iostream>
#include <string>


//CONSTANTS
const int monday = 0;
const int tuesday = 1;
const int wednesday = 2;
const int thursday = 3;
const int friday = 4;

const int FU = 0;
const int MCMILLIN = 1;
const int DAS = 2;
const int DAVIS = 3;
const int SABHARWAL = 4;
const int MARKOWSKY = 5;
const int PRICE = 6;
const int TAURITZ = 7;
const int LEOPOLD = 8;


//STRUCT
struct Suspect {
  int id;
  bool victim;
  bool insane;
  bool poor;
  std::string Location[5];
  bool friends[9];
};
Suspect SUSPECTS[9];

void stay(Suspect & A, const int day, const std::string location) {
  A.Location[day] = location;
}

void friends(Suspect & A, Suspect & B) {
  A.friends[B.id] = true;
  B.friends[A.id] = true;
}

bool friends_with(Suspect & A, Suspect & B) {
  return (A.friends[B.id] || B.friends[A.id]);
}

bool jealous(Suspect & A, Suspect & B) {
  for(int i = 0; i < 9; ++i) {
    if(A.friends[i] && B.friends[i]) {
      return true;
    }
  }
  return false;
}

bool motive(Suspect A) {
  return (jealous(A, SUSPECTS[LEOPOLD]) || A.insane || A.poor);
}

bool access(Suspect A) {
  bool wep_access = false;
  bool key_access = false;
  bool crime_access = false;
  if (A.Location[thursday] == "lab" || A.Location[wednesday] == "csOffice" || A.Location[wednesday] == "bookstore" || A.Location[thursday] == "bookstore") {
    wep_access = true;
  }

  if(A.Location[monday] == "csOffice" || A.Location[tuesday] == "lab" || A.id == DAVIS) {
    key_access = true;
  }

  if(A.Location[thursday] == "bookstore" || A.Location[friday] == "bookstore") {
    crime_access = true;
  }

  return (crime_access && key_access && wep_access);
}

bool murderer(Suspect A) {
  return (motive(A) && access(A));
}


int main(int argc, char* argv[]) {
  
  for(int i = 0; i < 9; ++i){
      SUSPECTS[i].id = i;
  }


  //All the Stay Fact Relations
  stay(SUSPECTS[FU], monday, "csOffice");
  stay(SUSPECTS[FU], monday, "csOffice");
  stay(SUSPECTS[FU], tuesday, "csOffice");
  stay(SUSPECTS[FU], wednesday, "lab");
  stay(SUSPECTS[FU], thursday, "csOffice");
  stay(SUSPECTS[FU], friday, "bookstore");
  stay(SUSPECTS[MCMILLIN], monday, "lab");
  stay(SUSPECTS[MCMILLIN], tuesday, "lab");
  stay(SUSPECTS[MCMILLIN], wednesday, "lab");
  stay(SUSPECTS[MCMILLIN], thursday, "csOffice");
  stay(SUSPECTS[MCMILLIN], friday, "bookstore");
  stay(SUSPECTS[DAS], monday, "bookstore");
  stay(SUSPECTS[DAS], tuesday, "lab");
  stay(SUSPECTS[DAS], wednesday, "bookstore");
  stay(SUSPECTS[DAS], thursday, "bookstore");
  stay(SUSPECTS[DAS], friday, "bookstore");
  stay(SUSPECTS[DAVIS], monday, "bookstore");
  stay(SUSPECTS[DAVIS], tuesday, "lab");
  stay(SUSPECTS[DAVIS], wednesday, "lab");
  stay(SUSPECTS[DAVIS], thursday, "csOffice");
  stay(SUSPECTS[DAVIS], friday, "bookstore");
  stay(SUSPECTS[SABHARWAL], monday, "bookstore");
  stay(SUSPECTS[SABHARWAL], tuesday, "bookstore");
  stay(SUSPECTS[SABHARWAL], wednesday, "csOffice");
  stay(SUSPECTS[SABHARWAL], thursday, "bookstore");
  stay(SUSPECTS[SABHARWAL], friday, "bookstore");
  stay(SUSPECTS[MARKOWSKY], monday, "bookstore");
  stay(SUSPECTS[MARKOWSKY], tuesday, "lab");
  stay(SUSPECTS[MARKOWSKY], wednesday, "lab");
  stay(SUSPECTS[MARKOWSKY], thursday, "bookstore");
  stay(SUSPECTS[MARKOWSKY], friday, "bookstore");
  stay(SUSPECTS[PRICE], monday, "csOffice");
  stay(SUSPECTS[PRICE], tuesday, "csOffice");
  stay(SUSPECTS[PRICE], wednesday, "lab");
  stay(SUSPECTS[PRICE], thursday, "csOffice");
  stay(SUSPECTS[PRICE], friday, "bookstore");
  stay(SUSPECTS[TAURITZ], monday, "bookstore");
  stay(SUSPECTS[TAURITZ], tuesday, "csOffice");
  stay(SUSPECTS[TAURITZ], wednesday, "csOffice");
  stay(SUSPECTS[TAURITZ], thursday, "csOffice");
  stay(SUSPECTS[TAURITZ], friday, "bookstore");

  SUSPECTS[SABHARWAL].insane = true;
  SUSPECTS[TAURITZ].insane = true;
  SUSPECTS[DAVIS].poor = true;
  SUSPECTS[FU].poor = true;
  SUSPECTS[TAURITZ].poor = true;
  SUSPECTS[PRICE].poor = true;
  
  friends(SUSPECTS[LEOPOLD], SUSPECTS[PRICE]);
  friends(SUSPECTS[PRICE], SUSPECTS[MCMILLIN]);
  friends(SUSPECTS[LEOPOLD], SUSPECTS[FU]);
  friends(SUSPECTS[FU], SUSPECTS[MARKOWSKY]);
  friends(SUSPECTS[MARKOWSKY], SUSPECTS[DAS]);
  friends(SUSPECTS[DAS], SUSPECTS[TAURITZ]);
  friends(SUSPECTS[SABHARWAL], SUSPECTS[TAURITZ]);
  friends(SUSPECTS[SABHARWAL], SUSPECTS[MCMILLIN]);



  for(int i = 0; i < 8; i++) {
    if(murderer(SUSPECTS[i])) {
      switch(i) {
        case FU: std::cout << "Murderer is FU\n"; break;
        case MCMILLIN: std::cout << "Murderer is MCMILLIN\n"; break;
        case DAS: std::cout << "Murderer is DAS\n"; break;
        case SABHARWAL: std::cout << "Murderer is SABHARWAL\n"; break;
        case MARKOWSKY: std::cout << "Murderer is MARKOWSKY\n"; break;
        case PRICE: std::cout << "Murderer is PRICE\n"; break;
        case TAURITZ: std::cout << "Murderer is TAURITZ\n"; break;
      }
    }
  }
  return 0;
}

