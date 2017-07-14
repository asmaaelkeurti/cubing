/**********************************************************************************************
* 命名空间: Cubing
* 类 名：   Point
* 创建日期：2017/6/29 4:00:17
*
* Ver   负责人  机器名    变更内容
* ────────────────────────────────────────────────
* V0.01 唐智英  LIWEIJUN-PC  初版
*
* Copyright (c)  NBA@Funmore.Inc.2017 Corporation. All rights reserved.
*┌───────────────────────────────────┐
*│　此技术信息为本公司机密信息，未经本公司书面同意禁止向第三方披露．　  │
*│　版权所有：安吉汽车物流有限公司智能物流事业部　　　　                │
*└───────────────────────────────────┘
*/
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Cubing
{
    /// <summary>
    /// 功 能：   中文功能的描述
    /// Function: 英文功能描述
    /// 修改时间、版本：2017/6/29 4:00:17/4.0.30319.42000
    /// 修改人： ANJI-CEVA/liweijun
    /// </summary>
    public class Point
    {
        public int x;
        public int y;
        public int z;

        public bool supported;
        public bool occupied;

        public Point(int X, int Y, int Z)
        {
            x = X;
            y = Y;
            z = Z;
        }
    }

    public class Option
    {
        public int x;
        public int y;
        public int z;

        public Option(int X, int Y, int Z)
        {
            x = X;
            y = Y;
            z = Z;
        }
    }
}
