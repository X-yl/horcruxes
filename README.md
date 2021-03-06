# horcruxes

[Totally unorignal](https://github.com/jesseduffield/horcrux), but [smaller and faster](#Performance).

`horcruxes` is a python package to split a file into `n` encrypted horcruxes, such that any `k` can be used to recreate the original file.

```
                    /————> filth.mp4_1_of_5.hcx 
                   /—————> filth.mp4_2_of_5.hcx —————\ 
  filth.mp4   ————<——————> filth.mp4_3_of_5.hcx ——————>———> filth.mp4
                   \—————> filth.mp4_4_of_5.hcx —————/
                    \————> filth.mp4_5_of_5.hcx 
                    
                              (n=5, k=3)
```



## How's it do that?
A secret is created and made into several shares using [Shamir's Secret Sharing](https://en.wikipedia.org/wiki/Shamir's_Secret_Sharing). Then, the secret is used to encrypt the content of the input file using AES-256.

Each horcrux file contains a short header and zero or more blocks of encrypted data. This data is then arranged in a "(k, 1) repetition code of blocks striped over n files".
As an example, for n=5, k=3, where the file has been divided into seven blocks, the following file structure is created:

| File 1 | File 2 | File 3 | File 4 | File 5 |
| ------ | ------ | ------ | ------ | ------ |
| a      | a      | a      | b      | b      |
| b      | c      | c      | c      | d      |
| d      | d      | e      | e      | e      |
| f      | f      | f      | g      | g      |
| g      | -      | -      | -      | -      |

Any three files together contain at least a single copy of every block without having to create 5 copies of each block.

## Performance
This module shows considerably faster and smaller results than [the one I stole the idea from](https://github.com/jesseduffield/horcrux).

Tested on a 1GB file, n=10, k=8:

#### File size
|                      | Mine  | Other | Ratio |
| -------------------- | ----- | ----- | ----- |
| Size per horcrux     | 300MB | 1GB   | 3.3   |
| Size for k horcruxes | 2.4GB | 8GB   | 3.3   |
| Size of n horcruxes  | 3 GB  | 10 GB | 3.3   |

The size per horcrux per horcrux is given by `original size * (n-k+1)/n`. The closer k is to n, the larger the size reduction.

#### Slower IO (HDD)
| Test  | Mine   | Other   | Ratio |
| ----- | ------ | ------- | ----- |
| split | 23.37s | 706.43s | 30.22 |
| bind  | 14.93s | 50.17s  | 3.36  |

#### Fast IO (SSD)
| Test  | Mine   | Other   | Ratio |
| ----- | ------ | ------- | ----- |
| split | 52.29s | 130.52s | 2.49  |
| bind  | 9.67s  | 11.73   | 1.213 |

This tool shows faster results in both cases, largely due to the fewer IO operations required, but also because AES is ridiculously optimized.

## Other improvements

It's now true to the actual Harry Potter lore, as you can create horcruxes with k=1.

## But why?

1. 

## Getting it

The entire repo is just a pip package, but it's also on PyPI:
```
pip install horcruxes
```

## Credits

It's an absolutely unoriginal idea.

https://github.com/jesseduffield/horcrux — same as mine, but slower

http://point-at-infinity.org/ssss/ — similar concept, not meant for files

https://github.com/kndyry/horcrux — not entirely the same, this one requires `n` = `k`