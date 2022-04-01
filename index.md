## Blockchain contact tracing app

The application of the experiment is designed according to hybrid architecture. A chosen centralized server and a decentralized blockchain in Ethereum is used. The tracing in the application is succeeded via the location of infected individuals.The health official completes a patient form with the patient's information and his condition. The patient's data are stored in the hospital's central server and blockchain.

<img src="https://github.com/Dimstella/blockchain-contact-tracing-app-hospitals/blob/main/image1.PNG" width="800" height="400" />

<p>All patients' data accompanied by doctor's notes are stored in a secure hospital database. At the same time, the postal code, country, the status of the patient (Infected, Suspected, Cured) are appended in a blockchain. Finally, to satisfy GDPR requirements, a hashing is generated and saved in both the central database as a primary key and blockchain as an id.</p>

img src="https://github.com/Dimstella/blockchain-contact-tracing-app-hospitals/blob/main/image2.PNG"  width="1200" height="400" />

<p>From a user perspective, the information streams are between the contact tracing web application and the blockchain. The user searches about infected people in the area based on postal code, country, and city. The app requests the blockchain. Each user search interacts only with the public blockchain of Ethereum. There is no interaction with the hospital's database to avoid privacy issues.</p>

<img src="https://github.com/Dimstella/blockchain-contact-tracing-app-hospitals/blob/main/image3.PNG"  width="1200" height="400" />

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

<h3>Smart Contract</h3>

``` Solidity
pragma solidity ^0.6.0;
pragma experimental ABIEncoderV2;

contract Contact_tracing {
    
    enum Statuses { Infected, Suspected, Cured }
    Statuses currentStatus;
    address owner;
    Patient patient;
    mapping(uint256 => Patient) personById;


      constructor() public{
      owner = msg.sender;
    }
      modifier ownerOnly(){
          require(msg.sender == owner);
          _;
    }

// Create a struct that saves the information of the infected person

    struct Patient {
        Statuses status;
        string postal;
        string hospitalName;
        string hashing;
        string country;
    }
        
    
    Patient[] public patients;
    
    function addPatient(Statuses _status, string memory _postal, string memory _hospitalName, string memory _hashing, string memory _country) public returns(uint) {

        patients.push(Patient(_status, _postal, _hospitalName, _hashing, _country));
        
        return patients.length;
    }

    function getPatientsCount() public view returns(uint) {
        return patients.length;
    }

    
    function gettPatient(uint index)  public view returns (Patient memory) {
        return patients[index];
    }
    

}
```
