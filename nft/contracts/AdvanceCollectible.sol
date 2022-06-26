//SPDX-Licence-Identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvanceCollectible is ERC721, VRFConsumerBase {

    bytes32 public keyHash;
    uint256 public fee;
    
    uint256 public randomResult;
    uint256 public tokenCounter;

    enum Breed{PUG, SHIBA_INU, ST_BERNARD}
    
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestToSender;

    event requestedCollectible(bytes32 indexed requestID, address requester);
    event breedAssigned(uint256 indexed tokenID, Breed breed);

    constructor(address _vrf, address _link, bytes32 _keyhash, uint256 _fee) public 
    VRFConsumerBase(
            _vrf, // VRF Coordinator
            _link  // LINK Token
    )
    ERC721(
        "Doggie",
        "Dog"
    )
    {
        tokenCounter = 0;
        keyHash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns(bytes32) {
        bytes32 requestID = requestRandomness(keyHash, fee);
        requestToSender[requestID] = msg.sender;

        emit requestedCollectible(requestID, msg.sender);

    }

    function fulfillRandomness(bytes32 requestID, uint256 randomNumber) internal override {
        Breed breed = Breed(randomNumber % 3); //random breed
        uint256 tokenID = tokenCounter;
        tokenIdToBreed[tokenID] = breed;

        emit breedAssigned(tokenID, breed);

        address owner = requestToSender[requestID];
        _safeMint(owner, tokenID);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenID, string memory tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokenID), "ERC721 caller is not owner or approved");
        _setTokenURI(tokenID, tokenURI);
    }
}