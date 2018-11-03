/*
 Navicat Premium Data Transfer

 Source Server         : fisher
 Source Server Type    : MySQL
 Source Server Version : 100134
 Source Host           : localhost:3306
 Source Schema         : fisher

 Target Server Type    : MySQL
 Target Server Version : 100134
 File Encoding         : 65001

 Date: 03/11/2018 09:57:35
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for drift
-- ----------------------------
DROP TABLE IF EXISTS `drift`;
CREATE TABLE `drift`  (
  `create_time` int(11) NULL DEFAULT NULL,
  `status` smallint(6) NULL DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `recipient_name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `address` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `message` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `mobile` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `isbn` varchar(13) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `book_title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `book_author` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `book_img` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `requester_id` int(11) NULL DEFAULT NULL,
  `requester_nickname` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `gifter_id` int(11) NULL DEFAULT NULL,
  `gift_id` int(11) NULL DEFAULT NULL,
  `gifter_nickname` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `pending` smallint(6) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of drift
-- ----------------------------
INSERT INTO `drift` VALUES (1535974548, 1, 4, 'chx', 'cccccccccccc', '', '13101746156', '9787531325093', '梦里花落知多少', '郭敬明', 'https://img1.doubanio.com/lpic/s1513378.jpg', 1, 'ch1996816', 2, 3, '帅比空', 3);
INSERT INTO `drift` VALUES (1535974674, 1, 5, 'chx', 'cccccccccccccccc', '', '13101746156', '9787501524044', '第一次的亲密接触', '蔡智恒', 'https://img3.doubanio.com/lpic/s1327750.jpg', 2, '帅比空', 1, 1, 'ch1996816', 4);
INSERT INTO `drift` VALUES (1535978251, 1, 6, 'chx', '666666666666666666', '', '13101746156', '9787531325093', '梦里花落知多少', '郭敬明', 'https://img1.doubanio.com/lpic/s1513378.jpg', 1, 'ch1996816', 2, 3, '帅比空', 2);
INSERT INTO `drift` VALUES (1535979586, 1, 7, 'chx', '1111111111111111111', '', '13101746156', '9787535434432', '悲伤逆流成河', '郭敬明', 'https://img3.doubanio.com/lpic/s2405994.jpg', 1, 'ch1996816', 2, 5, '帅比空', 2);
INSERT INTO `drift` VALUES (1535979993, 1, 8, 'chx', '6666666666666666', '', '13101746156', '9787020047697', '那些事，那些人', '郭敬明', 'https://img1.doubanio.com/lpic/s1670629.jpg', 1, 'ch1996816', 2, 6, '帅比空', 2);

-- ----------------------------
-- Table structure for gift
-- ----------------------------
DROP TABLE IF EXISTS `gift`;
CREATE TABLE `gift`  (
  `create_time` int(11) NULL DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NULL DEFAULT NULL,
  `isbn` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `launched` tinyint(1) NULL DEFAULT NULL,
  `status` smallint(6) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `uid`(`uid`) USING BTREE,
  CONSTRAINT `gift_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of gift
-- ----------------------------
INSERT INTO `gift` VALUES (NULL, 1, 1, '9787501524044', 0, 1);
INSERT INTO `gift` VALUES (1535765803, 2, 1, '9787531328858', 0, 1);
INSERT INTO `gift` VALUES (1535892856, 3, 2, '9787531325093', 1, 1);
INSERT INTO `gift` VALUES (1535893129, 4, 2, '9787531328858', 0, 1);
INSERT INTO `gift` VALUES (1535978470, 5, 2, '9787535434432', 1, 1);
INSERT INTO `gift` VALUES (1535979940, 6, 2, '9787020047697', 1, 1);
INSERT INTO `gift` VALUES (1535979964, 7, 2, '9787806277713', 0, 1);

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `create_time` int(11) NULL DEFAULT NULL,
  `status` smallint(6) NULL DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nickname` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `phone_number` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `confirmed` tinyint(1) NULL DEFAULT NULL,
  `beans` float NULL DEFAULT NULL,
  `send_counter` int(11) NULL DEFAULT NULL,
  `receive_counter` int(11) NULL DEFAULT NULL,
  `wx_open_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `wx_name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE,
  UNIQUE INDEX `phone_number`(`phone_number`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (NULL, 1, 1, 'ch1996816', NULL, 'pbkdf2:sha256:50000$PApKTt8q$c1a579095ade76c3ba3ba7b9ffe2984a9513bf513191d022d4fdd223d9512228', '331009573@qq.com', 0, 6, 0, 1, NULL, NULL);
INSERT INTO `user` VALUES (1535892732, 1, 2, '帅比空', NULL, 'pbkdf2:sha256:50000$JaZyho7r$bf6b33e606bc78a39069be72d27216472302498b606f469b22a61d7b46c01337', '979920817@qq.com', 0, 14.5, 2, 0, NULL, NULL);
INSERT INTO `user` VALUES (1535944149, 1, 3, 'chxfuqin', NULL, 'pbkdf2:sha256:50000$aY0DmTXC$ca487ebba7f32880b496a8bc02d4ed9bd40d86fd89834ee897b546dff34b879d', '909553467@qq.com', 0, 0, 0, 0, NULL, NULL);

-- ----------------------------
-- Table structure for wish
-- ----------------------------
DROP TABLE IF EXISTS `wish`;
CREATE TABLE `wish`  (
  `create_time` int(11) NULL DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NULL DEFAULT NULL,
  `isbn` varchar(15) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `launched` tinyint(1) NULL DEFAULT NULL,
  `status` smallint(6) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `uid`(`uid`) USING BTREE,
  CONSTRAINT `wish_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of wish
-- ----------------------------
INSERT INTO `wish` VALUES (1535787751, 1, 1, '9787535434432', 0, 1);
INSERT INTO `wish` VALUES (1535787764, 2, 1, '9787531325758', 0, 1);
INSERT INTO `wish` VALUES (1535979958, 3, 2, '9787532734160', 0, 1);
INSERT INTO `wish` VALUES (1535980613, 4, 1, '9787020047697', 1, 1);

SET FOREIGN_KEY_CHECKS = 1;
