# Technology primers (plain English, no company figures)

## AI data centers
Buildings filled with servers that train and run artificial-intelligence models. They need huge
amounts of computing chips, very fast connections between those chips, electricity and cooling.
The biggest buyers are the large cloud companies (often called hyperscalers). Their capital
spending (capex) plans are the main source of demand for most AI-hardware suppliers.

## GPU (graphics processing unit)
A chip that does thousands of simple calculations at the same time. It was designed to draw
video-game graphics, which is the same kind of maths (multiplying large tables of numbers) that
AI models need, so GPUs became the workhorse of AI. Analogy: a CPU is a few brilliant
mathematicians; a GPU is thousands of students each doing one easy sum at once. NVIDIA sells the
chips, complete server systems, the networking that links them, and CUDA, the software platform
developers use to program them; that software habit makes switching away harder.

## ASIC (custom chip)
A chip designed for one specific job, often built by or for a single cloud company. It can be
cheaper and more efficient than a general GPU for that job, which makes custom chips both a
competitor to GPUs and extra demand for the companies that connect chips together.

## Connecting the chips: why networking matters
Training a large model splits the work across thousands of chips that must constantly exchange
data. The links between them run at very high speeds (hundreds of gigabits per second per port,
moving to 800G and 1.6T generations). Two ways to carry the signal:
- **Copper** (electrical cables): cheap and power-efficient, but signals weaken quickly, so copper
  works only over short distances (a few metres, inside or between neighbouring racks).
- **Optical fibre** (light): carries data over long distances with little loss, but needs
  components that turn electrical signals into light and back, which cost more and use power.

## Optical transceiver
A small plug-in module at each end of a fibre cable. On the sending side a laser turns electrical
signals into flashes of light; on the receiving side a light detector turns them back. Analogy: two
people signalling with torches across a valley instead of shouting. Inside are lasers, light
detectors and a digital signal processor (DSP) that cleans up the signal. Companies like
Lumentum make lasers and other optical components; others assemble the modules.

## Active electrical cable (AEC)
A copper cable with a small chip at each end that boosts and cleans the signal, so copper can
carry today's very high speeds a few metres further than plain copper. Analogy: relay runners
passing the message on before it fades. It fills the gap between plain copper (too short) and
optics (more expensive and power-hungry) for connections inside and between racks.
Credo is a leading supplier.

## SerDes (serializer/deserializer)
The circuit inside a chip that turns many slow parallel data lanes into one very fast stream for
sending, and back again on arrival. Analogy: merging several lanes of traffic onto one high-speed
road and splitting them again at the exit. Every high-speed link depends on it.

## Endpoint security and security platforms (CrowdStrike)
Software that runs on laptops, servers and cloud workloads (the "endpoints") to detect and stop
attacks. Modern platforms send what each machine sees to the cloud, where software compares it
with what is happening across millions of machines to spot attacks. Customers pay yearly
subscriptions and often add modules over time: cloud security, identity protection, and SIEM
(security information and event management: collecting security logs from across a company to
detect threats). That is why recurring-revenue metrics (ARR) matter.

## Site development (Sterling Infrastructure)
Preparing a piece of land before a large building goes up: clearing, excavation, levelling,
foundations, and underground utilities (water, drainage, power conduits). Data centers,
warehouses and factories all need it, and big data-center campuses need a lot of it, quickly.
Analogy: building the plot, roads and plumbing before the house. Revenue comes from projects, so
backlog (signed work not yet done) is the key forward-looking number.
