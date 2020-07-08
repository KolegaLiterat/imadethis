using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices.WindowsRuntime;
using UnityEngine;
using UnityEngine.Tilemaps;

public class goalPoint : MonoBehaviour
{
    // Start is called before the first frame update
    [SerializeField]
    GameObject map;
    mapGenerator map_script;
    [SerializeField]
    GameObject endPoint;
    [SerializeField]
    GameObject road;
    [SerializeField]
    GameObject stringCutterObject;
    stringCutter stringCutterScript;
    [SerializeField]
    GameObject tilePointLight;
    public bool isGoalPointNeeded = true;
    const int maze_width = 9;
    const int maze_height = 9;
    List<int> oldGoalPointCoordinatest = new List<int>();
    void Start()
    {
        stringCutterScript = stringCutterObject.GetComponent<stringCutter>();
        map_script = map.GetComponent<mapGenerator>();
    }

    // Update is called once per frame
    void Update()
    {
        if (map_script.isMazeGenerated && isGoalPointNeeded)
        {
            add_goal_point();
        }

        /*
        if (Input.GetMouseButton(0))
        {
            isGoalPointNeeded = true;
            remove_old_goal_point();
        }
        */
    }

    void add_goal_point()
    {
        int index = -1;
        bool is_goal_point_different_from_recent = false;
        bool is_not_blocked_by_walls = false;
        GameObject[] road_tiles = GameObject.FindGameObjectsWithTag("road");
        GameObject road_tile = null;

        index = Random.Range(0, road_tiles.Length);

        if (index > -1 && index <= road_tiles.Length)
        {
            if (oldGoalPointCoordinatest.Count == 0)
            {
                road_tile = get_road_tile(road_tiles, index);
                set_goal_point(road_tile);
            } else
            {
                while (!is_goal_point_different_from_recent && !is_not_blocked_by_walls)
                {
                    road_tile = get_road_tile(road_tiles, index);
                    index = Random.Range(0, road_tiles.Length);
                    is_goal_point_different_from_recent = check_goal_points_corrdinatest(road_tile);
                    is_not_blocked_by_walls = check_walls(road_tile);
                }

                set_goal_point(road_tile);
            }

        } else
        {
            Debug.Log("Wrong index value!");
        }
    }

    GameObject get_road_tile(GameObject[] tiles, int index)
    {
        GameObject tile = tiles[index];

        return tile;
    }

    GameObject get_goal_point()
    {
        GameObject goal_point_tile = GameObject.FindGameObjectWithTag("goalPoint");

        return goal_point_tile;
    }

    void set_goal_point(GameObject tile)
    {
        List<int> coordinates = stringCutterScript.get_coordinates(tile.name);
        string tile_name = stringCutterScript.create_new_name(tile.name, "GoalPoint");

        float x_position = tile.transform.position.x;
        float y_position = tile.transform.position.y;
        float z_position = tile.transform.position.z;

        Destroy(map_script.map[coordinates[0], coordinates[1]]);
        map_script.map[coordinates[0], coordinates[1]] = (GameObject)Instantiate(endPoint, new Vector3(x_position, y_position, z_position), Quaternion.identity);
        map_script.map[coordinates[0], coordinates[1]].name = tile_name;
        map_script.map[coordinates[0], coordinates[1]].transform.SetParent(this.transform);

        add_light();

        isGoalPointNeeded = false;
    }

    public void remove_old_goal_point()
    {
        GameObject goal_point = get_goal_point();

        List<int> coordinates = stringCutterScript.get_coordinates(goal_point.name);
        save_old_goal_point_corrdinates(coordinates);
        string tile_name = stringCutterScript.create_new_name(goal_point.name, "Placeholder");

        float x_position = goal_point.transform.position.x;
        float y_position = goal_point.transform.position.y;
        float z_position = goal_point.transform.position.z;

        Destroy(map_script.map[coordinates[0], coordinates[1]]);

        map_script.map[coordinates[0], coordinates[1]] = (GameObject)Instantiate(road, new Vector3(x_position, y_position, z_position), Quaternion.identity);
        map_script.map[coordinates[0], coordinates[1]].name = tile_name;
        map_script.map[coordinates[0], coordinates[1]].transform.SetParent(map.transform);

        remove_light();
    }

    void save_old_goal_point_corrdinates(List<int> old_coordinates)
    {
        if (oldGoalPointCoordinatest.Count > 0)
        {
            oldGoalPointCoordinatest.Clear();
            oldGoalPointCoordinatest = old_coordinates;
        } else
        {
            oldGoalPointCoordinatest = old_coordinates;
        }
    }

    bool check_goal_points_corrdinatest(GameObject tile)
    {
        bool are_coordinates_different = false;
        List<int> new_coordinates = stringCutterScript.get_coordinates(tile.name);

        if (oldGoalPointCoordinatest[0] != new_coordinates[0])
        {
            if (oldGoalPointCoordinatest[1] != new_coordinates[1])
            {
                are_coordinates_different = true;
            }
        }

        return are_coordinates_different;
    }

    bool check_walls(GameObject tile)
    {
        bool is_goal_not_blocked = false;
        List<int> coordinates = stringCutterScript.get_coordinates(tile.name);
        int walls = 0;

        for (int i = 0; i > 4; i++)
        {
            switch (i)
            {
                case 0:
                    walls += count_walls_around_goal_point(1, 0, coordinates);
                    break;
                case 1:
                    walls += count_walls_around_goal_point(-1, 0, coordinates);
                    break;
                case 2:
                    walls += count_walls_around_goal_point(0, 1, coordinates);
                    break;
                case 3:
                    walls += count_walls_around_goal_point(0, -1, coordinates);
                    break;
                default:
                    break;
            }
        }

        if (walls <= 2)
        {
            is_goal_not_blocked = true;
        }

        return is_goal_not_blocked;
    }

    int count_walls_around_goal_point(int x_change, int y_change, List<int> goal_point_coordinate)
    {
        int wall = 0;
        int x_to_check = goal_point_coordinate[0] + x_change;
        int y_to_check = goal_point_coordinate[1] + y_change;

        if (x_to_check <= maze_width - 1 && x_to_check >= 0)
        {
            if (y_to_check <= maze_height - 1 && y_to_check >= 0)
            {
                if (map_script.map[x_to_check, y_to_check].tag == "wall")
                {
                    wall++;
                }
            }
        }

        return wall;
    }

    void add_light()
    {
        GameObject goal_point = GameObject.FindGameObjectWithTag("goalPoint");

        float x_light = goal_point.transform.position.x;
        float y_light = -5;
        float z_light = goal_point.transform.position.z;

        GameObject goal_point_light = (GameObject)Instantiate(tilePointLight, new Vector3(x_light, y_light, z_light), Quaternion.identity);
        goal_point_light.name = "goalPoint Light";
        goal_point_light.transform.SetParent(goal_point.transform);

    }
    void remove_light()
    {
        GameObject goal_point_light = GameObject.FindGameObjectWithTag("goalPointLight");

        Destroy(goal_point_light);
    }
}
