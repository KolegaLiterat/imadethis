using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class gui : MonoBehaviour
{   
    [SerializeField]
    palyer playerScript;
    [SerializeField]
    GameObject button;
    // Start is called before the first frame update
    void Start()
    {
        playerScript = playerScript.GetComponent<palyer>();

        if (playerScript.isPlayerAlive == true)
        {
            button.SetActive(false);
        }
    }

    // Update is called once per frame
    void Update()
    {   
        if (playerScript.isPlayerAlive == false)
        {
            button.SetActive(true);
        }
    }

    public void restartGame()
    {
        SceneManager.LoadScene("game");
    }
}
