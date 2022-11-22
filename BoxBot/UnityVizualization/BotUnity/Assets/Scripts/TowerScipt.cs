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
          pos.y = pos.y + 2;
          script.currPositions[box.name] = pos;

        }
        boxes.Add(other.gameObject);
      }
    }

    IEnumerator moveBox(GameObject box) {
      
      Vector3 nextPosition = box.transform.position;

      timer = timeToUpdate;

      nextPosition.y = nextPosition.y + 2;
      while (timer > 0)
      {
        Vector3 currentPosition = box.transform.position;
        timer -= Time.deltaTime;
        dt = 1.0f - (timer / timeToUpdate);
        Vector3 interpolated = Vector3.Lerp(currentPosition, nextPosition, dt);
        Vector3 direction = nextPosition - interpolated;

        box.transform.localPosition = interpolated;
        if(direction != Vector3.zero) box.transform.rotation = Quaternion.LookRotation(direction);

        // Yield here
        yield return null;
      }  
      // box.transform.position = nextPosition;
      yield return null;
    }
}
