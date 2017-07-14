using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Cubing;
using Newtonsoft.Json;
using System.IO;

namespace CubingTest
{
    class Program
    {
        static void Main(string[] args)
        {

            var cubing = new Cubing.Cubing();

            

            cubing.Boxes = generate_boxes(new Box(600,400,400), new Box(250,150,120), 200);
            var pallet = new LoadUnit(1000, 1200, 1200);
            cubing.loadUnit = pallet;

            cubing.cubing_FFD();

            File.WriteAllText(@"C:\Users\liweijun\Desktop\新建文件夹\Elkeurti\cubingData.json", JsonConvert.SerializeObject(cubing));
        }

        public static List<Box> generate_boxes(Box maxBox, Box minBox, int n)
        {
            var resultList = new List<Box>();

            Random rnd = new Random();

            for (int i = 0; i < n; i++)
            {
                resultList.Add(new Box(rnd.Next(minBox.x, maxBox.x)/20*20, rnd.Next(minBox.y, maxBox.y)/20*20, rnd.Next(minBox.z, maxBox.z)/20*20));
            } 
            

            return resultList;
        }

    }
}
