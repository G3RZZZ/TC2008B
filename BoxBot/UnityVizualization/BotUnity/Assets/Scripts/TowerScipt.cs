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
    Vector3 newPos;

    // Start is called before the first frame update
    void Start()
    {
      boxes = new List<GameObject>();
      newPos = new Vector3();
      agentController = GameObject.FindGameObjectWithTag("AgentController");
      script = agentController.GetComponent<AgentController>();
    }

    // Update is called once per frame
    void Update()
    {
      for (int i = 0; i < boxes.Count; i++)
      {
        float posY = .075f + .58f*(boxes.Count-(i+1));
        newPos = script.currPositions[boxes[i].name];
        newPos.y = posY;
        script.currPositions[boxes[i].name] = newPos;
      }
    }

    private void OnTriggerEnter(Collider other) {
      if (other.tag == "Box")
      {
        if (!boxes.Contains(other.gameObject))
        {
          boxes.Add(other.gameObject);
        }
      }
    }

}
