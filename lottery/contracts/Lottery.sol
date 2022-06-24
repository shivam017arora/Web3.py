//SPDX-Licence-Identifier: MIT

pragma solidity ^0.6.0;

// Get the latest ETH/USD price from chainlink price feed
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {

    address payable[] public players;
    uint256 public entryFeeInUSD;
    AggregatorV3Interface internal priceFeed;
    bytes32 public keyHash;
    uint256 public fee;
    address payable public recentWinner;
    uint256 public randomNumber;

    event RequestedRandomness(bytes32 requestId);

    enum LOTERRY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }

    LOTERRY_STATE public lottery_state;

    constructor(address _priceFeedAddress, address _vrf, address _link, uint256 _fee, bytes32 _keyhash) public VRFConsumerBase(_vrf, _link) {
        fee = _fee;
        keyHash = _keyhash;
        entryFeeInUSD = 50 * (10 ** 18);
        priceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTERRY_STATE.CLOSED; //1
    }

    //enter
    function enter() public payable {
        //require
        require(lottery_state == LOTERRY_STATE.OPEN);
        require(msg.value >= getEntranceFee(), "Not enough ETH!");
        //push
        players.push(msg.sender);
    }

    //get entrence fee
    function getEntranceFee() public view returns (uint256) {
        (, int price, , , ) = priceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10 ** 10;
        uint256 costEntranceFee =  (entryFeeInUSD * 10 ** 18) / uint256(adjustedPrice);
        return costEntranceFee;
    }

    //startLottery() onlyAdmin
    function startLottery() public onlyOwner {
        require(lottery_state == LOTERRY_STATE.CLOSED, "Lottery can't be open");
        lottery_state = LOTERRY_STATE.OPEN;
    }

    //endLottery() onlyAdmin
    function endLottery() public onlyOwner {
        lottery_state = LOTERRY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyHash, fee);
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override {
        require(lottery_state == LOTERRY_STATE.CALCULATING_WINNER, "You aren't there yet");
        require(_randomness > 0, "random-not-found");
        uint256 indexOfWinner = _randomness % players.length; //choose random winner
        recentWinner = players[indexOfWinner]; 
        recentWinner.transfer(address(this).balance); //transfer all balance to winner
        lottery_state = LOTERRY_STATE.CLOSED; //reset
        players = new address payable[](0); //reset
        randomNumber = _randomness;
    }
}