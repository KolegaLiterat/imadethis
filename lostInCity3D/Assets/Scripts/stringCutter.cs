using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;

public class stringCutter : MonoBehaviour
{

    string separator = "/";

    public string create_new_name(string old_tile_name, string tile_name)
    {
        string new_name = "0";
        string[] splitted = old_tile_name.Split('/');

        return new_name = tile_name + separator + splitted[1] + separator + splitted[2];
    }

    public List<int> get_coordinates(string tile_name)
    {
        List<int> coordinates = new List<int>();
        string[] splitted = tile_name.Split('/');
        int x = Int32.Parse(splitted[1]);
        int y = Int32.Parse(splitted[2]);

        coordinates.Add(x);
        coordinates.Add(y);

        return coordinates;
    }
}
