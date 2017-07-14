/**********************************************************************************************
* 命名空间: Cubing
* 类 名：   Cubing
* 创建日期：2017/6/30 4:15:05
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
    /// 修改时间、版本：2017/6/30 4:15:05/4.0.30319.42000
    /// 修改人： ANJI-CEVA/liweijun
    /// </summary>
    public class Cubing
    {
        public List<Box> Boxes;
        public LoadUnit loadUnit;
        public List<LoadUnit> loadUnits;

        public Cubing() { }

        public void cubing()
        {
            var NoOfPallet = 1;
            var testBoxes = new List<Box>(Boxes);
            testBoxes = testBoxes.OrderBy(box => box.x * box.y * box.z).Reverse().ToList();
            var testLoadUnit = new LoadUnit(loadUnit.x, loadUnit.y, loadUnit.z);

            loadUnits = new List<LoadUnit>();
            testLoadUnit.place_boxes(testBoxes);

            loadUnits.Add(testLoadUnit);
            
            while (loadUnits.Sum(loadUnit => loadUnit.PlacedBoxes.Count()) < Boxes.Count())
            {
                loadUnits = new List<LoadUnit>();
                testBoxes = new List<Box>(Boxes);
                NoOfPallet = NoOfPallet + 1;

                var splitedList = split(testBoxes, NoOfPallet);

                for (int i = 0; i < NoOfPallet; i++)
                {
                    var newLU = new LoadUnit(loadUnit.x, loadUnit.y, loadUnit.z);
                    loadUnits.Add(newLU);
                    testBoxes = splitedList[i].OrderBy(box => box.x * box.y * box.z).Reverse().ToList();
                    newLU.place_boxes(testBoxes);
                }
            }    
        }

        public static List<List<Box>> split(List<Box> boxes, int n)
        {
            var splitedList = new List<List<Box>>();

            for (int i = 0; i < n; i++)
            {
                splitedList.Add(new List<Box>());
            }

            var index = 0;

            foreach (var box in boxes)
            {
                splitedList[index % n].Add(box);
                index = index + 1;
            }

            return splitedList;

        }

        public void cubing_FFD()
        {
            var testBoxes = new List<Box>(Boxes);

            foreach (var box in testBoxes)
            {
                var newAvailableOption = new List<Option>();
                box.availableOption = box.availableOption.OrderBy(o => o.x * o.y).Reverse().Take(2).ToList();
            }


            testBoxes = testBoxes.OrderBy(box => Math.Max(Math.Max(box.x * box.y, box.x * box.z), Math.Max(box.y*box.z,box.x*box.y))).Reverse().ToList();
            var testLoadUnit = new LoadUnit(loadUnit.x, loadUnit.y, loadUnit.z);

            loadUnits = new List<LoadUnit>();
            loadUnits.Add(testLoadUnit);

            foreach (var box in testBoxes)
            {
                var i = 0;
                while (!loadUnits[i].place_box(box))
                {   
                    i = i + 1;
                    if (loadUnits.Count() < i + 1)
                    {
                        loadUnits.Add(new LoadUnit(loadUnit.x, loadUnit.y, loadUnit.z));
                    }
                }


            }

        }


    }
}
