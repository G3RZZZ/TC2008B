// Mateo Herrera - A01751912
// Gerardo Gutierrez - A01029422
// Francisco Salcedo -  A01633010
// Regina Rodriguez - A01284329

// Adapted from TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// By Octavio Navarro

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;


// Class that contains recieved iinformation of the model
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

// Class that contains recieved informamtion baout the models agents.
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

// Class that contains recieved information about robot agents
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

// Class that contains a list of AgentData classes
public class AgentsData
{
    public List<AgentData> positions;

    public AgentsData() => this.positions = new List<AgentData>();
}

// Class that contains a list  of RobotAgent classes
public class RobotsData
{
    public List<RobotData> positions;

    public RobotsData() => this.positions = new List<RobotData>();
}

public class AgentController : MonoBehaviour
{
    // Definition of get and post endpoints
    string serverUrl = "http://localhost:8585";
    string getAgentsEndpoint = "/getAgents";
    string getObstaclesEndpoint = "/getObstacles";
    string getBoxesEndpoint = "/getBoxes";
    string getTowersEndpoint = "/getTowers";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";

    // Declaration of variables
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
    [SerializeField] float max_time = 100;
    
    // Initialization of variables and data sent to model
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

      // Check if agents are still updating or simulation has reached the end
      if (keepRunning || updatedRobot || updatedBox)
      {
        // Ehen timer reaches , everything updates again.
        if(timer < 0 && keepRunning)
        {
            timer = timeToUpdate;
            updatedRobot = false;
            updatedBox = false;
            StartCoroutine(UpdateSimulation());
        }

        // When everything is done updating, positions are changed.
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
        }
      }
    }

    // Coroutine that updates the model. It fetches the update server endpoint,
    // and also starts the update robots and boxrs coroutines.
    IEnumerator UpdateSimulation()
    {
        float time = Time.realtimeSinceStartup;
        Debug.Log("Total Time: " + Time.realtimeSinceStartup);
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            modelData = JsonUtility.FromJson<ModelData>(www.downloadHandler.text);
            // If model sends back stop signal or max time is reached, 
            // simulation is stopped.
            if (!modelData.running || time > max_time)
            {
              keepRunning = false;
            }
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetBoxesData());
        }
    }

    // Initialization configuration is sent to the model in server. Initial 
    // positions of all models are fetched.
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

    // Coroutiene that fetches robot agent data.
    IEnumerator GetAgentsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getAgentsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            // Robot data is stored in a list of RobotData classes
            robotsData = JsonUtility.FromJson<RobotsData>(www.downloadHandler.text);
            float steps = 0;

            // New agaent positions are stored in dictionaries. Previous positions
            // are stored as well.  The position where the roboy should be looking at
            // is also stored in a dictionary.
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

                        // Y value is kept the same as before.
                        if(agents.TryGetValue(agent.id, out currentY)) {
                          newAgentPosition.y = agents[agent.id].transform.position.y;
                        }
                        currPositions[agent.id] = newAgentPosition;
                    }
            }
            Debug.Log("Total moves made by the robots: " + steps);
            updatedRobot = true;
            if(!startedRobot) startedRobot = true;
        }
    }

    // Coroutine that fetches box agent data. It is the same as the robot agent coroutine,
    // except the data returned by the server is less.
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
                        // Y value is kept the same
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

    // Coroutine that fetches obstacle agent data. This coroutine is only called once
    // since obstacles do not move.
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

    // Coroutine that fetches tower agent data. This coroutine is only called once
    // since obstacles do not move.
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
