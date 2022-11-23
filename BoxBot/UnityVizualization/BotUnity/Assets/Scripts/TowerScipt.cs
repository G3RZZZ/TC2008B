// Mateo Herrera - A01751912
// Gerardo Gutierrez - A01029422
// Francisco Salcedo -  A01633010
// Regina Rodriguez - A01284329

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TowerScipt : MonoBehaviour
{
    // Declaration of variables
    List<GameObject> boxes;
    public float timeToUpdate = 5.0f;
    private float timer, dt;
    GameObject agentController;
    AgentController script;
    Vector3 newPos;

    // Start is called before the first frame update
    void Start()
    {
      // Initialization of variables
      boxes = new List<GameObject>();
      newPos = new Vector3();
      agentController = GameObject.FindGameObjectWithTag("AgentController");
      script = agentController.GetComponent<AgentController>();
    }

    // Boxes in list are moved upwards in relation to how many boxes there are in
    // the tower.
    void Update()
    {
      for (int i = 0; i < boxes.Count; i++)
      {
        float posY = .075f + .58f*(boxes.Count-(i+1));
        // float posY = .075f + .58f*(i);
        newPos = script.currPositions[boxes[i].name];
        newPos.y = posY;
        script.currPositions[boxes[i].name] = newPos;
      }
    }

    // When boxes enter collider, they are stored in a list.
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
