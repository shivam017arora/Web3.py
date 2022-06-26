# NFTs: On-Chain and Off-Chain Metadata

We are aware that Ethereum 2.0 will solve a lot of these scaling headaches (also CONGRATULATIONS TO Eth 2.0 FOR A SUCCESSFUL LAUNCH), but for now, the community needed a standard to help with this. Metadata is this help.

Metadata provides descriptive information for a tokenId that is stored off-chain. These are simple APIs that off-chain UIs call to gather all the information about the token. Each tokenId has a specific tokenURI that defines this API call, which returns a JSON object that looks something like this:

Metadata:

```
{
"name": "You NFT token name",
"description": "Something Cool here",
"image": "https://ipfs.io/ipfs/QmTgqnhFBMkfT9s8PHKcdXBn1f5bG3Q5hmBaR4U6hoTvb1?filename=Chainlink_Elf.png",
"attributes": [. . .]
}
```

<b> <u>
It’s important that if your NFT interacts with other NFTs to make sure that the attributes on the tokenURI match the attributes of your NFT smart contract, otherwise you may get confused when the interactions happen!
</b> </u>
<br />
<br />

You can always store all your metadata on-chain (in fact, that’s the only way for your tokens to interact), but a lot of NFT marketplaces don’t know how to read on-chain metadata \_yet. \_So for the time being, using the off-chain metadata to visualize your token, while having all the on-chain metadata is ideal so your tokens can interact with each other.

The name, description, and attributes are easy to store on-chain, but the image is the hard part. Also, where do we store this API for the tokenURI? A lot of people choose to run servers to host the information, which is great, but it is a centralized place for visualizing the token. It would be better if we could store our images on-chain so that they can’t go down or get hacked. You’ll notice in the example above, their image is using a URL that points to IPFS, and this is a popular way to store images.

IPFS stands for InterPlanetary File System and is a peer-to-peer hypermedia protocol designed to make the web faster, safer, and more open. It allows anyone to upload a file, and that file is hashed so that if it changes, so does its hash. This is ideal for storing images since it means that every time the image is updated, the on-chain hash/tokenURI also has to change, meaning that we can have a record of the history of the metadata. It’s also really easy to add an image onto IPFS and doesn’t require running a server!

Here is what we will be doing:

1. Build a verifiably random D&D character using the Chainlink VRF
2. Add a tokenURI using IPFS
3. Adding your randomized NFTs to the OpenSea Marketplace

This repo at the moment only works with Rinkeby, so please be sure to jump to Rinkeby!

Opensea: https://testnets.opensea.io/assets/rinkeby/0xBf3aa9AA1d2853506695BcD0a00C73827d5Dc7a0/0
IPFS: ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json
Rinkey Contract: 0xBf3aa9AA1d2853506695BcD0a00C73827d5Dc7a0
Etherscan: https://rinkeby.etherscan.io/address/0xBf3aa9AA1d2853506695BcD0a00C73827d5Dc7a0
