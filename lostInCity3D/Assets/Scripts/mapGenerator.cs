using System.Collections;
using System.Collections.Generic;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;

public class mapGenerator : MonoBehaviour
{
    public bool isMazeGenerated = false;
    
    [SerializeField]
    GameObject tile;
    [SerializeField]
    GameObject road;
    [SerializeField]
    GameObject building;
    [SerializeField]
    GameObject stringHelperObject;
    [SerializeField]
    Text percent;
    [SerializeField]
    Text loading;
    stringCutter stringCutterScript;

    public GameObject[,] map;
    GameObject[] placeholders;
    bool isStartingPointOnMap = false;
    
    int x_position = 0, y_position = 0;
    public float x_position_for_player = 0, y_position_for_player = 0, z_position_for_player;
    const int maze_width = 9;
    const int maze_height = 9;
    void Start()
    {
        stringCutterScript = stringHelperObject.GetComponent<stringCutter>();
        placeholder_map_generator();
    }
    void Update()
    {
        if (!isMazeGenerated)
        {
            generate_maze();
        } else
        {
            percent.gameObject.SetActive(false);
            loading.gameObject.SetActive(false);
        }
    }

    void placeholder_map_generator()
    {
        float offset_x = 2.5f, offset_z = -2.5f;
        int i, j;

        map = new GameObject[maze_width, maze_height];

        for (i = 0; i < maze_width; i++)
        {
            for (j = 0; j < maze_height; j++)
            {
                map[i, j] = (GameObject)Instantiate(tile, new Vector3(tile.transform.position.x + offset_x * i, tile.transform.position.y, tile.transform.position.z + offset_z * j), Quaternion.identity);
                string object_name = "Placeholder/" + i + "/" + j;
                map[i, j].name = object_name;
                map[i, j].transform.SetParent(this.transform);
            }

        }
    }

    void generate_maze()
    {
        GameObject next_tile = null;
        placeholders = GameObject.FindGameObjectsWithTag("placeholder");

        calculate_percents(81);

        if (!isStartingPointOnMap)
        {
            x_position = Random.Range(0, 9);
            y_position = Random.Range(0, 9);
            set_starting_point(x_position, y_position);
            isStartingPointOnMap = true;
        }

        if (placeholders.Length != 0)
        {
            next_tile = get_next_tile();
            
            if (next_tile != null)
            {
                create_new_element_of_maze(next_tile, placeholders.Length);
            } else
            {
                Debug.Log("Next tile is NULL! Check return variable in get_next_tile_method");
;           }

        } else {  
            isMazeGenerated = true;
        }
    }

    void set_starting_point(int start_x, int start_y)
    {
        float x_position = map[start_x, start_y].transform.position.x;
        float y_position = map[start_x, start_y].transform.position.y;
        float z_position = map[start_x, start_y].transform.position.z;

        x_position_for_player = x_position;
        y_position_for_player = y_position + 2;
        z_position_for_player = z_position;

        string tile_name = stringCutterScript.create_new_name(map[start_x, start_y].name, "Road");

        Destroy(map[start_x, start_y]);

        map[start_x, start_y] = (GameObject)Instantiate(road, new Vector3(x_position, y_position, z_position), Quaternion.identity);
        map[start_x, start_y].name = tile_name;
        map[start_x, start_y].transform.SetParent(this.transform);

    }

    GameObject get_next_tile()
    {
        int direction;
        GameObject tile = null;

        while (tile == null)
        {
            direction = Random.Range(0, 4);

            switch (direction)
            {
                case 0:
                    tile = get_obejct_on_coordinates(-1, 0);
                    break;
                case 1:
                    tile = get_obejct_on_coordinates(1, 0);
                    break;
                case 2:
                    tile = get_obejct_on_coordinates(0, -1);
                    break;
                case 3:
                    tile = get_obejct_on_coordinates(0, 1);
                    break;
                default:
                    break;
            }
        }

        return tile;
    }

    GameObject get_obejct_on_coordinates(int x_change, int y_change)
    {
        GameObject object_on_map = null;

        int x_position_to_check = x_position + x_change;
        int y_position_to_check = y_position + y_change;

        if (x_position_to_check <= maze_width - 1 && x_position_to_check >= 0)
        {
            if (y_position_to_check <= maze_height - 1 && y_position_to_check >= 0)
            {
                object_on_map = map[x_position_to_check, y_position_to_check];
                x_position = x_position_to_check;
                y_position = y_position_to_check;
            }
        }
        return object_on_map;
    }

    void create_new_element_of_maze(GameObject tile, int placeholders_amount)
    {
        int can_create_tile = Random.Range(0, 2);
        float tile_x = tile.transform.position.x;
        float tile_y = tile.transform.position.y;
        float tile_z = tile.transform.position.z;

        if (placeholders_amount <= 10)
        {
            can_create_tile = 1;
        }

        if (tile.tag == "placeholder")
        {
            if (check_surrinding_tiles())
            {
                string tile_name = stringCutterScript.create_new_name(map[x_position, y_position].name, "Wall");

                Destroy(map[x_position, y_position]);
                
                map[x_position, y_position] = (GameObject)Instantiate(building, new Vector3(tile_x, tile_y, tile_z), Quaternion.identity);
                map[x_position, y_position].name = tile_name; 
                map[x_position, y_position].transform.SetParent(this.transform);
            } else
            {
                
                if (can_create_tile == 1)
                {
                    string tile_name = stringCutterScript.create_new_name(map[x_position, y_position].name, "Road");
                    
                    Destroy(map[x_position, y_position]);

                    map[x_position, y_position] = (GameObject)Instantiate(road, new Vector3(tile_x, tile_y, tile_z), Quaternion.identity);
                    map[x_position, y_position].name = tile_name;
                    map[x_position, y_position].transform.SetParent(this.transform);
                }
                
            }

        }
    }

    bool check_surrinding_tiles()
    {
        bool is_wall_can_be_created = false;
        int road_tiles = 0;

        for (int i = 0; i < 4; i++)
        {
            switch (i)
            {
                case 0:
                    road_tiles += count_road_tiles(-1, 0);
                    break;
                case 1:
                    road_tiles += count_road_tiles(1, 0);
                    break;
                case 2:
                    road_tiles += count_road_tiles(0, -1);
                    break;
                case 3:
                    road_tiles += count_road_tiles(0, 1);
                    break;
                default:
                    break;
            }
        }

        if (road_tiles >= 3)
        {
            is_wall_can_be_created = true;
        }

        return is_wall_can_be_created;
    }

    int count_road_tiles(int x_change, int y_change)
    {
        int road_tile = 0;

        int x_position_to_check = x_position + x_change;
        int y_position_to_check = y_position + y_change;

        if (x_position_to_check <= maze_width - 1 && x_position_to_check >= 0)
        {
            if (y_position_to_check <= maze_height - 1 && y_position_to_check >= 0)
            {
                if (map[x_position_to_check, y_position_to_check].tag == "road")
                {
                    road_tile++;
                }
            }
        }
        return road_tile;
    }

    void calculate_percents(int number_of_placeholders)
    {
        int number_of_roads = GameObject.FindGameObjectsWithTag("road").Length;
        int percents = 100 * number_of_roads / number_of_placeholders;
        string loading_text = percents.ToString() + "%";

        Debug.Log(loading_text);

        percent.text = loading_text;
    }
} 
