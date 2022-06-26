// SPDX-Licence-Identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;
    constructor() public ERC721("Doggie", "Dog") {
        tokenCounter = 0;
    }

    function createCollectible(string memory tokenURI) public returns (uint256) {
        uint256 tokenID = tokenCounter;
        _safeMint(msg.sender, tokenID);
        tokenCounter = tokenCounter + 1;
        _setTokenURI(tokenID, tokenURI);
        return tokenID;
    }

}