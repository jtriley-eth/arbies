// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

// memory : value
// 0x0000 : balanceOf.selector | getReserves.selector
// 0x0004 : balanceOf.arg0
// 0x0024 : token0.balanceOf(uniswap)
// 0x0044 : token1.balanceOf(uniswap)
// 0x0064 : token0.balanceOf(sushiswap)
// 0x0084 : token1.balanceOf(sushiswap)
// 0x00a4 : token0.balanceOf(shibaswap)
// 0x00c4 : token1.balanceOf(shibaswap)
// 0x00e4 : token0.balanceOf(croswap)
// 0x0104 : token1.balanceOf(croswap)
// 0x0124 : uniswap.getReserves()[0]
// 0x0144 : uniswap.getReserves()[1]
// 0x0164 : sushiswap.getReserves()[0]
// 0x0184 : sushiswap.getReserves()[1]
// 0x01a4 : shibaswap.getReserves()[0]
// 0x01c4 : shibaswap.getReserves()[1]
// 0x01e4 : croswap.getReserves()[0]
// 0x0204 : croswap.getReserves()[1]
contract Recon {
    uint256 constant internal token0 = 0x006b175474e89094c44da98b954eedeac495271d0f;
    uint256 constant internal token1 = 0x00c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2;
    uint256 constant internal uniswap = 0x00a478c2975ab1ea89e8196811f51a7b7ade33eb11;
    uint256 constant internal sushiswap = 0x00c3d03e4f041fd4cd388c549ee2a29a9e5075882f;
    uint256 constant internal shibaswap = 0x008faf958e36c6970497386118030e6297fff8d275;
    uint256 constant internal croswap = 0x0060a26d69263ef43e9a68964ba141263f19d71d51;

    constructor() {
        assembly {
            mstore(0x00, 0x70a0823100000000000000000000000000000000000000000000000000000000)

            mstore(0x04, uniswap)
            pop(staticcall(gas(), token0, 0x00, 0x24, 0x0024, 0x20))
            pop(staticcall(gas(), token1, 0x00, 0x24, 0x0044, 0x20))

            mstore(0x04, sushiswap)
            pop(staticcall(gas(), token0, 0x00, 0x24, 0x0064, 0x20))
            pop(staticcall(gas(), token1, 0x00, 0x24, 0x0084, 0x20))

            mstore(0x04, shibaswap)
            pop(staticcall(gas(), token0, 0x00, 0x24, 0x00a4, 0x20))
            pop(staticcall(gas(), token1, 0x00, 0x24, 0x00c4, 0x20))

            mstore(0x04, croswap)
            pop(staticcall(gas(), token0, 0x00, 0x24, 0x00e4, 0x20))
            pop(staticcall(gas(), token1, 0x00, 0x24, 0x0104, 0x20))

            mstore(0x00, 0x0902f1ac00000000000000000000000000000000000000000000000000000000)

            pop(staticcall(gas(), uniswap,   0x00, 0x04, 0x0124, 0x40))
            pop(staticcall(gas(), sushiswap, 0x00, 0x04, 0x0164, 0x40))
            pop(staticcall(gas(), shibaswap, 0x00, 0x04, 0x01a4, 0x40))
            pop(staticcall(gas(), croswap,   0x00, 0x04, 0x01e4, 0x40))

            return(0x24, 0x0200)
        }
    }
}

