// SPDX-License-Identifier: MIT
pragma solidity 0.8.24;

contract Runner {
    uint256 constant internal me = 0x00b47A9B6F062c33ED78630478dFf9056687F840f2;
    uint256 constant internal token0 = 0x006b175474e89094c44da98b954eedeac495271d0f;
    uint256 constant internal token1 = 0x00c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2;
    uint256 constant internal uniswap = 0x00a478c2975ab1ea89e8196811f51a7b7ade33eb11;
    uint256 constant internal sushiswap = 0x00c3d03e4f041fd4cd388c549ee2a29a9e5075882f;
    uint256 constant internal shibaswap = 0x008faf958e36c6970497386118030e6297fff8d275;
    uint256 constant internal croswap = 0x0060a26d69263ef43e9a68964ba141263f19d71d51;

    constructor() payable {
        assembly {
            let success := 1
            mstore(0x00, 0x095ea7b300000000000000000000000000000000000000000000000000000000)
            mstore(0x04, not(0x00))
            success := and(success, call(gas(), token0, 0x00, 0x00, 0x24, 0x00, 0x44))
            success := and(success, mload(0x44))
            success := and(success, call(gas(), token1, 0x00, 0x00, 0x24, 0x00, 0x44))
            success := and(success, mload(0x44))
            if iszero(success) { revert(0x00, 0x00) }
        }
    }

    fallback() external payable {
        assembly {
            let success := eq(caller(), me)
            let word := calldataload(0x00)

            mstore(0x00, token1)
            mstore(0x20, token0)
            let zeroForOne := shr(0xff, word)
            let token := mload(shl(0x05, zeroForOne))

            mstore(0x00, uniswap)
            mstore(0x20, sushiswap)
            mstore(0x40, shibaswap)
            mstore(0x80, croswap)
            let dex0 := mload(shl(0x05, and(0x03, shr(253, word))))
            let dex1 := mload(shl(0x05, and(0x03, shr(251, word))))

            mstore(0x00, 0xa9059cbb00000000000000000000000000000000000000000000000000000000)
            mstore(0x04, dex0)
            mstore(0x24, shr(0x05, shl(0x05, word)))
            success := and(success, call(gas(), token, 0x00, 0x00, 0x44, 0x00, 0x20))
            success := and(success, mload(0x00))

            mstore(0x00, 0x022c0d9f00000000000000000000000000000000000000000000000000000000)
            mstore(0x04, 0x00)
            mstore(0x24, 0x00)
            mstore(0x44, dex1)
            mstore(0x64, 0x80)
            mstore(0x84, 0x00)
            mstore(add(0x04, shl(0x05, iszero(zeroForOne))), calldataload(0x20))
            success := and(success, call(gas(), dex0, 0x00, 0x00, 0xa4, 0x00, 0x00))

            mstore(0x04, 0x00)
            mstore(0x24, 0x00)
            mstore(0x44, address())
            mstore(add(0x04, shl(0x05, zeroForOne)), calldataload(0x40))
            success := and(success, call(gas(), dex1, 0x00, 0x00, 0xa4, 0x00, 0x00))

            if success { stop() }
            revert(0x00, 0x00)
        }
    }

    receive() external payable { }
}
