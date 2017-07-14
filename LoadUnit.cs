/**********************************************************************************************
* 命名空间: Cubing
* 类 名：   LoadUnit
* 创建日期：2017/6/29 3:58:03
*
* Ver   负责人  机器名    变更内容
* ────────────────────────────────────────────────
* V0.01 李维钧  LIWEIJUN-PC  初版
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
    /// 修改时间、版本：2017/6/29 3:58:03/4.0.30319.42000
    /// 修改人： ANJI-CEVA/liweijun
    /// </summary>
    public class LoadUnit
    {
        public int x;
        public int y;
        public int z;

        public List<Point> AvailablePoints;

        public List<Box> PlacedBoxes;

        public LoadUnit(int length, int width, int height)
        {
            x = length;
            y = width;
            z = height;

            AvailablePoints = new List<Point>() { new Point(0,0,0)};

            PlacedBoxes = new List<Box>();
        }

        public bool place_box(Box box)
        {
            foreach (var option in box.availableOption)
            {
                AvailablePoints = AvailablePoints.OrderBy(point => point.z).ThenBy(point => point.y).ThenBy(point => point.x).ToList();
                foreach (var point in AvailablePoints)
                {
                    if (checkSpace(option, point))
                    {
                        box.bestOption = option;
                        box.startPoint = point;

                        PlacedBoxes.Add(box);

                        AvailablePoints.Remove(point);

                        foreach (var corner in find_corners(point, option))
                        {
                            if (check_if_corner(corner)) { AvailablePoints.Add(corner); }
                        }
                        return true;
                    }
                }

            }

            return false;
        }



        public void place_boxes(List<Box> boxes)
        {
            foreach (var box in boxes)
            {
                var isBreaked = false;
                foreach (var option in box.availableOption)
                {
                    AvailablePoints = AvailablePoints.OrderBy(point => point.x).ThenBy(point => point.y).ThenBy(point => point.z).ToList();

                    foreach (var point in AvailablePoints)
                    {
                        if (checkSpace(option, point))
                        {
                            box.bestOption = option;
                            box.startPoint = point;

                            PlacedBoxes.Add(box);

                            AvailablePoints.Remove(point);

                            foreach (var corner in find_corners(point, option))
                            {
                                if (check_if_corner(corner)) { AvailablePoints.Add(corner); }
                            }


                            isBreaked = true;
                            break;
                        }
                    }
                    if (isBreaked) { break; }
                }


            }


        }

        public bool checkSpace(Option option, Point startPoint)
        {
            List<Point> corners = find_support_points(startPoint, option);
            var occupyPoints = find_occupy_points(startPoint, option);

            foreach (var point in corners)
            {
                check_point_status(point);
            }

            foreach (var point in occupyPoints)
            {
                check_point_status(point);
            }


            return (corners.Count(point => point.supported == true) == 4) && !occupyPoints.Any(point => point.occupied == true);
        }

        public static List<Point> find_corners(Point sp, Option o)
        {
            var corners = new List<Point>();
            corners.Add(new Point(sp.x + o.x, sp.y, sp.z));
            corners.Add(new Point(sp.x + o.x, sp.y + o.y, sp.z));
            corners.Add(new Point(sp.x, sp.y + o.y, sp.z));
            corners.Add(new Point(sp.x + o.x, sp.y, sp.z + o.z));
            corners.Add(new Point(sp.x + o.x, sp.y + o.y, sp.z + o.z));
            corners.Add(new Point(sp.x, sp.y, sp.z + o.z));
            corners.Add(new Point(sp.x, sp.y + o.y, sp.z + o.z));

            corners.Add(sp);

            return corners;
        }

        public static List<Point> find_support_points(Point sp, Option o)
        {
            var corners = new List<Point>();
            corners.Add(new Point(sp.x + o.x - 1, sp.y + 1, sp.z));
            corners.Add(new Point(sp.x + o.x - 1, sp.y + o.y - 1, sp.z));
            corners.Add(new Point(sp.x + 1, sp.y + o.y - 1, sp.z));
            corners.Add(new Point(sp.x + 1, sp.y + 1, sp.z));


            return corners;
        }

        public static List<Point> find_occupy_points(Point sp, Option o)
        {
            var corners = new List<Point>();
            corners.Add(new Point(sp.x + o.x - 1, sp.y + 1, sp.z + 1));
            corners.Add(new Point(sp.x + o.x - 1, sp.y + o.y - 1, sp.z + 1));
            corners.Add(new Point(sp.x + 1, sp.y + o.y - 1, sp.z + 1));
            corners.Add(new Point(sp.x + 1, sp.y + 1, sp.z + 1));

            corners.Add(new Point(sp.x + o.x/2 - 1, sp.y + 1, sp.z + 1));
            corners.Add(new Point(sp.x + o.x - 1, sp.y + o.y/2 - 1, sp.z + 1));
            corners.Add(new Point(sp.x + 1, sp.y + o.y/2 - 1, sp.z + 1));
            corners.Add(new Point(sp.x + o.x/2 - 1, sp.y + o.y/2 - 1, sp.z + 1));

            corners.Add(new Point(sp.x + o.x*2 / 3, sp.y + o.y / 2 - 1, sp.z + 1));
            corners.Add(new Point(sp.x + o.x / 3 - 1, sp.y + o.y / 2 - 1, sp.z + 1));

            corners.Add(new Point(sp.x + 1, sp.y + 1, sp.z + o.z - 1));
            corners.Add(new Point(sp.x + o.x - 1, sp.y + 1, sp.z + o.z - 1));

            corners.Add(new Point(sp.x + 1, sp.y + o.y - 1, sp.z + o.z - 1));

            corners.Add(new Point(sp.x + o.x - 1, sp.y + o.y - 1, sp.z + o.z - 1));

            corners.Add(sp);

            return corners;
        }

        public void check_point_status(Point point)
        {
            if (point.x > this.x || point.y > this.y || point.z > this.z || point.x < 0 || point.y < 0 || point.z < 0)
            {
                point.occupied = true;
                point.supported = false;
            }
            else
            {
                point.occupied = PlacedBoxes.Any(
                    box => 
                        (box.startPoint.x < point.x && (box.startPoint.x + box.bestOption.x) > point.x)
                        &&(box.startPoint.y < point.y && (box.startPoint.y + box.bestOption.y) > point.y)
                        &&(box.startPoint.z < point.z && (box.startPoint.z + box.bestOption.z) > point.z)

                    );

                if (point.z == 0)
                {
                    point.supported = true;
                }
                else
                {
                    point.supported = PlacedBoxes.Any(
                        box =>
                            (box.startPoint.x <= point.x && (box.startPoint.x + box.bestOption.x) >= point.x)
                            && (box.startPoint.y <= point.y && (box.startPoint.y + box.bestOption.y) >= point.y)
                            &&(box.startPoint.z + box.bestOption.z == point.z)
                            
                            
                        );
                }
            }


            




        }

        public bool check_if_corner(Point corner)
        {
            var c1 = new Point(corner.x - 1, corner.y - 1, corner.z - 1);
            var c2 = new Point(corner.x + 1, corner.y - 1, corner.z - 1);
            var c3 = new Point(corner.x + 1, corner.y + 1, corner.z - 1);
            var c4 = new Point(corner.x - 1, corner.y + 1, corner.z - 1);
            var c5 = new Point(corner.x - 1, corner.y - 1, corner.z + 1);
            var c6 = new Point(corner.x + 1, corner.y - 1, corner.z + 1);
            var c7 = new Point(corner.x + 1, corner.y + 1, corner.z + 1);
            var c8 = new Point(corner.x - 1, corner.y + 1, corner.z + 1);

            var corners = new List<Point>() { c1, c2, c3, c4, c5, c6, c7, c8 };

            foreach (var c in corners)
            {
                check_point_status(c);
            }

            return (corners.Count(c => c.occupied == false) >= 1);

            


        }

    }
}
