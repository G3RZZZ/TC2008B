using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TowerScipt : MonoBehaviour
{
    
    List<GameObject> boxes;
    public float timeToUpdate = 5.0f;
    private float timer, dt;
    GameObject agentController;
    AgentController script;
    // Start is called before the first frame update
    void Start()
    {
      boxes = new List<GameObject>();
      agentController = GameObject.FindGameObjectWithTag("AgentController");
      script = agentController.GetComponent<AgentController>();
    }

    // Update is called once per frame
    void Update()
    {

    }

    private void OnTriggerEnter(Collider other) {
      if (other.tag == "Box")
      {
        foreach (var box in boxes)
        {
          Vector3 pos = script.prevPositions[box.name];
          pos.y = pos.y + .58f;
          script.currPositions[box.name] = pos;

        }
        boxes.Add(other.gameObject);
      }
    }

}
