using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class palyer : MonoBehaviour
{
    public bool isPlayerAlive = true;
    [SerializeField]
    mapGenerator mapScript;
    [SerializeField]
    goalPoint goalPointScript;
    bool isPlayerSet = false;
    [SerializeField]
    Vector3 direction;
    [SerializeField]
    GameObject playerLight;
    [SerializeField]
    Text score;
    [SerializeField]
    Text playerHealth;
    int healthLeft = 100;
    int points = 0;
    float playerSpeed = 0.2f;
    Rigidbody rb;

    void Start()
    {
        score.text = "Points: " + points;
        playerHealth.text = "Health: " + healthLeft;
        mapScript = GameObject.FindGameObjectWithTag("map").GetComponent<mapGenerator>();
        goalPointScript = GameObject.FindGameObjectWithTag("goalPointScript").GetComponent<goalPoint>();
        rb = this.GetComponent<Rigidbody>();
    }

    // Update is called once per frame
    void Update()
    {
        score.text = "Points: " + points;
        playerHealth.text = "Health: " + healthLeft;

        if (!isPlayerSet && mapScript.isMazeGenerated)
        {
            transform.position = new Vector3(mapScript.x_position_for_player, mapScript.y_position_for_player, mapScript.z_position_for_player);
            add_light();
            isPlayerSet = true;
        }

        if (isPlayerSet && healthLeft > 0)
        {
            isPlayerAlive = true;

            if (Input.GetKey(KeyCode.W))
            {
                direction = Vector3.forward;
            }

            if (Input.GetKey(KeyCode.S))
            {
                direction = Vector3.back;
            }

            if (Input.GetKey(KeyCode.A))
            {
                direction = Vector3.left;
            }

            if (Input.GetKey(KeyCode.D))
            {
                direction = Vector3.right;
            }
        } else
           
        if (healthLeft <= 0)
        {
            isPlayerAlive = false;
        }
  
        move_light();
        stop_player();
    }

    void move_player(Vector3 direction)
    {
        rb.AddForce(direction * playerSpeed * Time.fixedTime);
    }

    void add_light()
    {
        float x_light = this.transform.position.x;
        float y_light = -0.5f;
        float z_light = this.transform.position.z;

        GameObject player_light = (GameObject)Instantiate(playerLight, new Vector3(x_light, y_light, z_light), playerLight.transform.rotation);
        player_light.name = "Player Spotlight";
        player_light.transform.SetParent(this.transform);
    }

    void move_light()
    {
        playerLight.transform.Translate(this.transform.position.x, -0.5f, this.transform.position.z);

    }

    void stop_player()
    {
        if (transform.position.z <= -12.0f || transform.position.z >= 12.0f || transform.position.x >= 19.5f || transform.position.x <= -4.5f)
        {
            rb.useGravity = true;
            rb.constraints = RigidbodyConstraints.None;
            rb.velocity = Vector3.zero;
            rb.angularVelocity = Vector3.zero;
            transform.Rotate(10.0f, 10.0f, 10.0f);
            healthLeft = 0;
        }
    }

    private void FixedUpdate()
    {
        move_player(direction);
        stop_player();
    }

    private void OnTriggerEnter(Collider other)
    {
        goalPointScript.isGoalPointNeeded = true;
        goalPointScript.remove_old_goal_point();
        add_point();
        add_health();
    }

    private void OnCollisionEnter(Collision collision)
    {
        remove_health();
    }

    void add_point()
    {
        points += 1;
    }
    
    void add_health()
    {
        healthLeft += 3;
    }

    void remove_health()
    {
        healthLeft -= 1;
    }

}
