// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2021

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class ModelData
{
    public string message;
    public float currentStep;
    public bool running;

    public ModelData(string message, float currentStep, bool running)
    {
      this.message = message;
      this.currentStep = currentStep;
      this.running = running;
    }
}

[Serializable]
public class AgentData
{
    public string id;
    public float x, y, z;

    public AgentData(string id, float x, float y, float z)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
    }
}
[Serializable]
public class RobotData
{
    public string id;
    public float steps_taken, x, y, z, xl, zl;

    public RobotData(string id, float steps_taken, float x, float xl, float y, float z,  float zl)
    {
        this.id = id;
        this.steps_taken = steps_taken;
        this.x = x;
        this.xl = xl;
        this.y = y;
        this.z = z;
        this.zl = zl;
    }
}

[Serializable]

public class AgentsData
{
    public List<AgentData> positions;

    public AgentsData() => this.positions = new List<AgentData>();
}

public class RobotsData
{
    public List<RobotData> positions;

    public RobotsData() => this.positions = new List<RobotData>();
}

public class AgentController : MonoBehaviour
{
    // private string url = "https://agents.us-south.cf.appdomain.cloud/";
    string serverUrl = "http://localhost:8585";
    string getAgentsEndpoint = "/getAgents";
    string getObstaclesEndpoint = "/getObstacles";
    string getBoxesEndpoint = "/getBoxes";
    string getTowersEndpoint = "/getTowers";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    public AgentsData agentsData, obstacleData;
    public RobotsData robotsData;
    public ModelData modelData;
    Dictionary<string, GameObject> agents;
    public Dictionary<string, Vector3> prevPositions, currPositions, lookPositions;

    bool updatedRobot = false, startedRobot = false, updatedBox = false, startedBox = false, keepRunning = true;

    public GameObject agentPrefab, obstaclePrefab, boxPrefab, towerPrefab, floor;
    public int NAgents, width, height, NTowers;
    public float timeToUpdate = 5.0f;
    private float timer, dt;

    void Start()
    {
        agentsData = new AgentsData();
        robotsData = new RobotsData();
        obstacleData = new AgentsData();

        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();
        lookPositions = new Dictionary<string, Vector3>();

        agents = new Dictionary<string, GameObject>();

        floor.transform.localScale = new Vector3((float)width/10, 1, (float)height/10);
        floor.transform.localPosition = new Vector3((float)width/2-0.5f, 0, (float)height/2-0.5f);
        
        timer = timeToUpdate;

        StartCoroutine(SendConfiguration());
    }

    private void Update() 
    {

      if (keepRunning || updatedRobot || updatedBox)
      {
        if(timer < 0 && keepRunning)
        {
            timer = timeToUpdate;
            updatedRobot = false;
            updatedBox = false;
            StartCoroutine(UpdateSimulation());
        }

        if (updatedRobot && updatedBox)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            foreach(var agent in currPositions)
            {
                Vector3 currentPosition = agent.Value;
                Vector3 previousPosition = prevPositions[agent.Key];
                Vector3 lookPosition = lookPositions[agent.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = lookPosition - interpolated;

                agents[agent.Key].transform.localPosition = interpolated;
                if(direction != Vector3.zero && currentPosition.y <= 0.075) agents[agent.Key].transform.rotation = Quaternion.LookRotation(direction);
            }

            // float t = (timer / timeToUpdate);
            // dt = t * t * ( 3f - 2f*t);
        }
      }
    }
 
    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            modelData = JsonUtility.FromJson<ModelData>(www.downloadHandler.text);
            if (!modelData.running)
            {
              Debug.Log("Total Time: " + Time.realtimeSinceStartup);
              keepRunning = false;
            }
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetBoxesData());
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("NAgents", NAgents.ToString());
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());
        form.AddField("NTowers", NTowers.ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetObstacleData());
            StartCoroutine(GetBoxesData());
            StartCoroutine(GetTowersData());
        }
    }

    IEnumerator GetAgentsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getAgentsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            robotsData = JsonUtility.FromJson<RobotsData>(www.downloadHandler.text);
            float steps = 0;

            foreach(RobotData agent in robotsData.positions)
            {

                    Vector3 newAgentPosition = new Vector3(agent.x, agent.y, agent.z);
                    Vector3 newLookPosition = new Vector3(agent.xl, agent.y, agent.zl);
                    lookPositions[agent.id] = newLookPosition;
                    steps+= agent.steps_taken;
                    if(!startedBox)
                    {
                        prevPositions[agent.id] = newAgentPosition;
                        agents[agent.id] = Instantiate(agentPrefab, newAgentPosition, Quaternion.identity);
                        agents[agent.id].name = agent.id;
                    }
                    else
                    {
                        Vector3 currentPosition = new Vector3();
                        GameObject currentY;
                        if(currPositions.TryGetValue(agent.id, out currentPosition)){
                            newAgentPosition.y = currPositions[agent.id].y;
                            prevPositions[agent.id] = currentPosition;
                        }

                        if(agents.TryGetValue(agent.id, out currentY)) {
                          newAgentPosition.y = agents[agent.id].transform.position.y;
                        }
                        currPositions[agent.id] = newAgentPosition;
                    }
            }
            Debug.Log("Total steps Taken: " + steps);
            updatedRobot = true;
            if(!startedRobot) startedRobot = true;
        }
    }

    IEnumerator GetBoxesData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getBoxesEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            agentsData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            foreach(AgentData agent in agentsData.positions)
            {

                    Vector3 newAgentPosition = new Vector3(agent.x, agent.y, agent.z);
                    lookPositions[agent.id] = newAgentPosition;
                    if(!startedBox)
                    {
                        prevPositions[agent.id] = newAgentPosition;
                        agents[agent.id] = Instantiate(boxPrefab, newAgentPosition, Quaternion.identity);
                        agents[agent.id].name = agent.id;
                    }
                    else
                    {
                        Vector3 currentPosition = new Vector3();
                        if(currPositions.TryGetValue(agent.id, out currentPosition)){
                            newAgentPosition.y = currPositions[agent.id].y;
                            prevPositions[agent.id] = currentPosition;
                        }
                        newAgentPosition.y = agents[agent.id].transform.position.y;
                        currPositions[agent.id] = newAgentPosition;
                    }
            }

            updatedBox = true;
            if(!startedBox) startedBox = true;
        }
    }

    IEnumerator GetObstacleData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getObstaclesEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            obstacleData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            Debug.Log(obstacleData.positions);

            foreach(AgentData obstacle in obstacleData.positions)
            {
                Instantiate(obstaclePrefab, new Vector3(obstacle.x, obstacle.y, obstacle.z), Quaternion.identity);
            }
        }
        
    }

    IEnumerator GetTowersData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getTowersEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            obstacleData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            Debug.Log(obstacleData.positions);

            foreach(AgentData obstacle in obstacleData.positions)
            {
                Instantiate(towerPrefab, new Vector3(obstacle.x, obstacle.y, obstacle.z), Quaternion.identity);
            }
        }
        
    }
}
